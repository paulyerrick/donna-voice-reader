#!/usr/bin/env python3
"""Donna — Voice Reader desktop app."""

import sys
import os
import io
import json
import threading
import webview
from flask import Flask, request, jsonify, Response

# ─── Paths (dev + PyInstaller bundle) ─────────────────────────────────────────
def get_app_root():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

APP_ROOT = get_app_root()
STATIC_FOLDER = os.path.join(APP_ROOT, 'static')
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

app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path='')

DEFAULT_CONFIG = {
    "openai_api_key": "",
    "elevenlabs_api_key": "",
    "cartesia_api_key": "",
    "default_provider": "openai",
    "selected_voice": "",
    "account_tier": "free",
}

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            cfg = DEFAULT_CONFIG.copy()
            cfg.update(json.load(f))
            return cfg
    return DEFAULT_CONFIG.copy()

def save_config(cfg):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(cfg, f, indent=2)

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
import urllib.request
import urllib.error

CARTESIA_API_VERSION = '2026-03-01'
CARTESIA_MODEL_ID = 'sonic-3.5'

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
            return resp.read()  # raw mp3 bytes
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8', errors='replace')
        raise ValueError(f"OpenAI API error {e.code}: {err_body}")

def tts_elevenlabs(text, voice, cfg):
    """ElevenLabs TTS via direct HTTP."""
    api_key = cfg.get('elevenlabs_api_key', '')
    if not api_key:
        raise ValueError("ElevenLabs API key not set. Add it in Settings.")
    # voice is the voice_id
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
        err_body = e.read().decode('utf-8', errors='replace')
        raise ValueError(f"ElevenLabs API error {e.code}: {err_body}")

def tts_cartesia(text, voice, cfg):
    """Cartesia TTS via direct HTTP (websocket-free, uses REST chunked endpoint)."""
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
        err_body = e.read().decode('utf-8', errors='replace')
        raise ValueError(f"Cartesia API error {e.code}: {err_body}")

PROVIDERS = {
    'openai': tts_openai,
    'elevenlabs': tts_elevenlabs,
    'cartesia': tts_cartesia,
}

# ─── Routes ───────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/voices')
def get_voices():
    cfg = load_config()
    catalog = load_voice_catalog()
    return jsonify({
        'openai': voices_for_provider('openai', cfg),
        'elevenlabs': voices_for_provider('elevenlabs', cfg),
        'cartesia': voices_for_provider('cartesia', cfg),
        'account_tier': get_account_tier(cfg),
        'beta_all_free': catalog.get('beta_all_free', False),
    })

@app.route('/api/config', methods=['GET'])
def get_config():
    cfg = load_config()
    # Return which keys are set (not the actual keys)
    return jsonify({
        "openai_set": bool(cfg.get('openai_api_key')),
        "elevenlabs_set": bool(cfg.get('elevenlabs_api_key')),
        "cartesia_set": bool(cfg.get('cartesia_api_key')),
        "default_provider": cfg.get('default_provider', 'openai'),
        "selected_voice": cfg.get('selected_voice', ''),
        "account_tier": get_account_tier(cfg),
    })

@app.route('/api/config', methods=['POST'])
def set_config():
    data = request.json
    cfg = load_config()
    for key in ['openai_api_key', 'elevenlabs_api_key', 'cartesia_api_key']:
        if key in data and data[key]:
            cfg[key] = data[key]
    if 'default_provider' in data:
        cfg['default_provider'] = data['default_provider']
    if 'selected_voice' in data:
        cfg['selected_voice'] = data['selected_voice']
    save_config(cfg)
    return jsonify({"ok": True})

@app.route('/api/tts', methods=['POST'])
def synthesize():
    data = request.json
    text = data.get('text', '').strip()
    provider = data.get('provider', 'openai')
    voice = data.get('voice', '')
    if not text:
        return jsonify({"error": "No text provided"}), 400
    if provider not in PROVIDERS:
        return jsonify({"error": f"Unknown provider: {provider}"}), 400

    cfg = load_config()
    if not is_voice_allowed(provider, voice, cfg):
        return jsonify({"error": "That voice is not available on your plan."}), 400

    try:
        audio_bytes = PROVIDERS[provider](text, voice, cfg)
        return Response(io.BytesIO(audio_bytes), mimetype='audio/mpeg',
                        headers={'Content-Disposition': 'inline; filename="tts.mp3"'})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500

# ─── Desktop launcher ─────────────────────────────────────────────────────────
def start_server():
    import time
    # Brief delay so the window opens before first request
    time.sleep(0.3)
    app.run(host='127.0.0.1', port=17895, debug=False, use_reloader=False)

def _reset_macos_dock_icon():
    """Force bundle icon (masked) instead of the unmasked executable embedded icon."""
    import time
    time.sleep(0.8)
    try:
        import AppKit
        AppKit.NSApp().setApplicationIconImage_(None)
    except Exception:
        pass


def main():
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Create native window
    webview.create_window(
        'Donna - Voice Reader',
        'http://127.0.0.1:17895',
        width=960,
        height=900,
        min_size=(640, 700),
        text_select=True,
        frameless=True,
        easy_drag=True,
    )
    # Don't pass icon on macOS — webview overrides the bundle icon with an unmasked
    # square image while running. CFBundleIconFile (Donna.icns) handles the Dock.
    if sys.platform == 'darwin':
        webview.start(_reset_macos_dock_icon)
    else:
        icon = ICON_PATH if os.path.isfile(ICON_PATH) else None
        webview.start(icon=icon)
    # When window closes, exit
    os._exit(0)

if __name__ == '__main__':
    main()