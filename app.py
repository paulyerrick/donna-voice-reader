#!/usr/bin/env python3
"""Donna — Voice Reader desktop app."""

import sys
import os
import io
import json
import secrets
import threading
import webview
import urllib.request
import urllib.error
from flask import Flask, request, jsonify, Response

# ─── Paths (dev + PyInstaller bundle) ─────────────────────────────────────────
def get_app_root():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

APP_ROOT = get_app_root()
STATIC_FOLDER = os.path.join(APP_ROOT, 'static')
INDEX_HTML_PATH = os.path.join(STATIC_FOLDER, 'index.html')
VOICES_CATALOG_PATH = os.path.join(APP_ROOT, 'voices.json')
ICON_PATH = os.path.join(APP_ROOT, 'assets', 'Donna.icns')
if not os.path.isfile(ICON_PATH):
    ICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'Donna.icns')

def get_config_dir():
    if sys.platform == 'darwin':
        base = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'Donna')
    else:
        base = os.path.join(os.path.expanduser('~'), '.donna')
    os.makedirs(base, exist_ok=True)
    return base

CONFIG_PATH = os.path.join(get_config_dir(), 'config.json')
TOKEN_PATH = os.path.join(get_config_dir(), '.api_token')

app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path='')

API_TOKEN = secrets.token_urlsafe(32)
MAX_TTS_CHARS = 8000
FLUID_SCHEMES = frozenset({'donna', 'ocean', 'sunset', 'forest', 'mono'})
_index_html_cache = None

DEFAULT_CONFIG = {
    "openai_api_key": "",
    "elevenlabs_api_key": "",
    "cartesia_api_key": "",
    "default_provider": "local",
    "selected_voice": "",
    "account_tier": "free",
    "fluid_scheme": "donna",
    "fluid_reactive": True,
}

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            os.chmod(CONFIG_PATH, 0o600)
        except OSError:
            pass
        with open(CONFIG_PATH) as f:
            cfg = DEFAULT_CONFIG.copy()
            cfg.update(json.load(f))
            return cfg
    return DEFAULT_CONFIG.copy()

def save_config(cfg):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(cfg, f, indent=2)
    try:
        os.chmod(CONFIG_PATH, 0o600)
    except OSError:
        pass

def require_api_token():
    if request.headers.get('X-Donna-Token') != API_TOKEN:
        return jsonify({"error": "Forbidden"}), 403
    return None

def get_json_body():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None
    return data

def provider_http_error(provider_name, status_code):
    raise ValueError(f"{provider_name} API error ({status_code}). Check your API key and try again.")

# ─── Curated voice catalog (edit voices.json to change offerings) ─────────────
_voice_catalog_cache = None

def load_voice_catalog():
    global _voice_catalog_cache
    if _voice_catalog_cache is None:
        with open(VOICES_CATALOG_PATH, encoding='utf-8') as f:
            _voice_catalog_cache = json.load(f)
    return _voice_catalog_cache

def get_account_tier(cfg):
    return cfg.get('account_tier', 'free')

def voices_for_provider(provider, cfg):
    """Return voices available to this user. Beta unlocks premium; free tier gets 5 curated voices."""
    catalog = load_voice_catalog()
    prov = catalog.get('providers', {}).get(provider, {})
    free = prov.get('free', [])
    premium = prov.get('premium', [])
    tier = get_account_tier(cfg)
    if catalog.get('beta_all_free') or tier in ('beta', 'premium'):
        return free + premium
    return free

def is_voice_allowed(provider, voice_id, cfg):
    return any(v['id'] == voice_id for v in voices_for_provider(provider, cfg))

# ─── TTS Providers ────────────────────────────────────────────────────────────
CARTESIA_API_VERSION = '2026-03-01'
CARTESIA_MODEL_ID = 'sonic-3.5'

def tts_local(text, voice, cfg):
    """Local neural TTS via bundled Kokoro-82M (Apache 2.0)."""
    from kokoro_engine import synthesize, VOICE_FILES

    voices = [v['id'] for v in voices_for_provider('local', cfg)]
    if voice not in voices:
        voice = voices[0] if voices else "af_heart"
    if voice not in VOICE_FILES:
        voice = "af_heart"
    return synthesize(text, voice, APP_ROOT)

def tts_openai(text, voice, cfg):
    """OpenAI TTS via direct HTTP (no SDK dependency)."""
    api_key = cfg.get('openai_api_key', '')
    if not api_key:
        raise ValueError("OpenAI API key not set. Add it in Settings.")
    voices = [v['id'] for v in voices_for_provider('openai', cfg)]
    if voice not in voices:
        voice = voices[0] if voices else "alloy"
    url = "https://api.openai.com/v1/audio/speech"
    body = json.dumps({
        "model": "gpt-4o-mini-tts",
        "input": text,
        "voice": voice,
        "response_format": "mp3",
    }).encode()
    req = urllib.request.Request(url, data=body, headers={
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        provider_http_error("OpenAI", e.code)

def tts_elevenlabs(text, voice, cfg):
    """ElevenLabs TTS via direct HTTP."""
    api_key = cfg.get('elevenlabs_api_key', '')
    if not api_key:
        raise ValueError("ElevenLabs API key not set. Add it in Settings.")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"
    body = json.dumps({
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    }).encode()
    req = urllib.request.Request(url, data=body, headers={
        'xi-api-key': api_key,
        'Content-Type': 'application/json',
        'Accept': 'audio/mpeg',
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        provider_http_error("ElevenLabs", e.code)

def tts_cartesia(text, voice, cfg):
    """Cartesia TTS via direct HTTP."""
    api_key = cfg.get('cartesia_api_key', '')
    if not api_key:
        raise ValueError("Cartesia API key not set. Add it in Settings.")
    url = "https://api.cartesia.ai/tts/bytes"
    body = json.dumps({
        "model_id": CARTESIA_MODEL_ID,
        "transcript": text,
        "voice": {"mode": "id", "id": voice},
        "output_format": {
            "container": "mp3",
            "sample_rate": 44100,
            "bit_rate": 128000,
        },
    }).encode()
    req = urllib.request.Request(url, data=body, headers={
        'X-API-Key': api_key,
        'Cartesia-Version': CARTESIA_API_VERSION,
        'Content-Type': 'application/json',
        'Accept': 'audio/mpeg',
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        provider_http_error("Cartesia", e.code)

PROVIDERS = {
    'local': tts_local,
    'openai': tts_openai,
    'elevenlabs': tts_elevenlabs,
    'cartesia': tts_cartesia,
}

# ─── Routes ───────────────────────────────────────────────────────────────────
def get_index_html():
    global _index_html_cache
    if _index_html_cache is None:
        with open(INDEX_HTML_PATH, encoding='utf-8') as f:
            body = f.read()
        inject = f'<script>window.__DONNA_API_TOKEN={json.dumps(API_TOKEN)};</script>'
        _index_html_cache = body.replace('</head>', inject + '\n</head>', 1)
    return _index_html_cache

@app.route('/')
def index():
    return Response(get_index_html(), mimetype='text/html')

@app.route('/api/voices')
def get_voices():
    cfg = load_config()
    catalog = load_voice_catalog()
    return jsonify({
        'local': voices_for_provider('local', cfg),
        'openai': voices_for_provider('openai', cfg),
        'elevenlabs': voices_for_provider('elevenlabs', cfg),
        'cartesia': voices_for_provider('cartesia', cfg),
        'account_tier': get_account_tier(cfg),
        'beta_all_free': catalog.get('beta_all_free', False),
    })

@app.route('/api/config', methods=['GET'])
def get_config():
    cfg = load_config()
    return jsonify({
        "openai_set": bool(cfg.get('openai_api_key')),
        "elevenlabs_set": bool(cfg.get('elevenlabs_api_key')),
        "cartesia_set": bool(cfg.get('cartesia_api_key')),
        "default_provider": cfg.get('default_provider', 'local'),
        "selected_voice": cfg.get('selected_voice', ''),
        "account_tier": get_account_tier(cfg),
        "fluid_scheme": cfg.get('fluid_scheme', 'donna'),
        "fluid_reactive": cfg.get('fluid_reactive', True),
    })

@app.route('/api/config', methods=['POST'])
def set_config():
    denied = require_api_token()
    if denied:
        return denied
    data = get_json_body()
    if data is None:
        return jsonify({"error": "Invalid JSON body"}), 400

    cfg = load_config()
    for key in ['openai_api_key', 'elevenlabs_api_key', 'cartesia_api_key']:
        if key in data:
            cfg[key] = str(data[key]).strip()
    if 'default_provider' in data:
        provider = data['default_provider']
        if provider not in PROVIDERS:
            return jsonify({"error": f"Unknown provider: {provider}"}), 400
        cfg['default_provider'] = provider
    if 'selected_voice' in data:
        cfg['selected_voice'] = str(data['selected_voice']).strip()
    if 'fluid_scheme' in data:
        scheme = data['fluid_scheme']
        if scheme not in FLUID_SCHEMES:
            return jsonify({"error": f"Unknown theme: {scheme}"}), 400
        cfg['fluid_scheme'] = scheme
    if 'fluid_reactive' in data:
        cfg['fluid_reactive'] = bool(data['fluid_reactive'])
    save_config(cfg)
    return jsonify({"ok": True})

@app.route('/api/tts', methods=['POST'])
def synthesize():
    denied = require_api_token()
    if denied:
        return denied
    data = get_json_body()
    if data is None:
        return jsonify({"error": "Invalid JSON body"}), 400

    text = str(data.get('text', '')).strip()
    provider = data.get('provider', 'openai')
    voice = str(data.get('voice', '')).strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400
    if len(text) > MAX_TTS_CHARS:
        return jsonify({"error": f"Text too long (max {MAX_TTS_CHARS} characters)"}), 400
    if provider not in PROVIDERS:
        return jsonify({"error": f"Unknown provider: {provider}"}), 400

    cfg = load_config()
    if not is_voice_allowed(provider, voice, cfg):
        return jsonify({"error": "That voice is not available on your plan."}), 400

    try:
        audio_bytes = PROVIDERS[provider](text, voice, cfg)
        if provider == 'local':
            mime = 'audio/wav'
            filename = 'tts.wav'
        else:
            mime = 'audio/mpeg'
            filename = 'tts.mp3'
        return Response(io.BytesIO(audio_bytes), mimetype=mime,
                        headers={'Content-Disposition': f'inline; filename="{filename}"'})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Speech generation failed. Please try again."}), 500

# ─── Desktop launcher ─────────────────────────────────────────────────────────
def start_server():
    import time
    time.sleep(0.3)
    app.run(host='127.0.0.1', port=17895, debug=False, use_reloader=False)


class DonnaApi:
    """JS bridge for native window actions."""

    def toggle_fullscreen(self):
        window = webview.active_window()
        if window:
            window.toggle_fullscreen()


def main():
    try:
        with open(TOKEN_PATH, 'w', encoding='utf-8') as f:
            f.write(API_TOKEN)
        os.chmod(TOKEN_PATH, 0o600)
    except OSError:
        pass

    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    webview.create_window(
        'Donna - Voice Reader',
        'http://127.0.0.1:17895',
        width=960,
        height=900,
        min_size=(640, 700),
        text_select=True,
        frameless=True,
        easy_drag=True,
        js_api=DonnaApi(),
    )
    icon = ICON_PATH if os.path.isfile(ICON_PATH) else None
    webview.start(icon=icon)
    os._exit(0)

if __name__ == '__main__':
    main()
