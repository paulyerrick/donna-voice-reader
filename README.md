# Donna Voice Reader

A macOS desktop app that reads text aloud with natural voices. Paste or type text, press play, and listen — with a reactive WebGL fluid background that responds to the audio.

**Default voices run fully offline** via bundled [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) (Apache 2.0). Cloud providers are optional.

## Download & install

1. Go to **[Releases](https://github.com/paulyerrick/donna-voice-reader/releases)** and download **Donna-Voice-Reader-*-macOS.dmg** (recommended) or the ZIP.
2. Open the DMG and drag **Donna** to **Applications**.
3. **First launch:** Donna is not code-signed. Right-click **Donna** in Applications → **Open** → **Open** again to confirm.

The download is ~1.2 GB because it includes the local neural TTS model and runtime.

## Quick start

1. Launch **Donna**.
2. Paste or type text in the main field.
3. Press **Play** (or `⌘↩` / Space when the text field is not focused).
4. Use **Settings** (gear icon) to pick a voice, theme, or cloud provider.

**Local voices** (Settings → Provider → **Local**) work with no API key. For OpenAI, ElevenLabs, or Cartesia, add your API key under Settings → Provider.

## Features

- **Offline TTS** — five curated Kokoro voices, no account required
- **Cloud TTS** — OpenAI, ElevenLabs, and Cartesia (API keys in Settings)
- **Reactive background** — WebGL fluid shader with audio-reactive motion (toggle in Settings)
- **Themes** — Donna, Ocean, Sunset, Forest, Mono
- **Playback controls** — play/pause, skip ±10 seconds

## Keyboard shortcuts

| Shortcut | Action |
|----------|--------|
| `⌘↩` | Play / pause |
| Space | Play / pause (when text field is not focused) |
| `⌘F` | Toggle fullscreen |

## Requirements

- **macOS** 13 or later
- **Optional:** API keys for cloud providers only

Config is stored at `~/Library/Application Support/Donna/config.json`.

## Build from source

Requires **Python 3.10–3.12** (3.13+ is not supported by the Kokoro stack).

```bash
git clone https://github.com/paulyerrick/donna-voice-reader.git
cd donna-voice-reader
./build_mac.sh
open dist/Donna.app
```

`build_mac.sh` creates a venv, installs dependencies, downloads Kokoro model weights into `assets/kokoro/`, and runs PyInstaller.

### Development

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./scripts/download_kokoro_assets.sh   # once, for local voices
python app.py
```

The dev server runs at `http://127.0.0.1:17895` inside a pywebview window.

## Release packaging

Maintainers with [GitHub CLI](https://cli.github.com/) authenticated:

```bash
./scripts/publish_release.sh v0.2.0
```

This builds `Donna.app`, creates DMG + ZIP under `release/`, and publishes to GitHub Releases.

## Project layout

| Path | Purpose |
|------|---------|
| `app.py` | Flask API + pywebview desktop shell |
| `kokoro_engine.py` | Local Kokoro TTS synthesis |
| `static/index.html` | UI (fluid shader, glass panels, settings) |
| `voices.json` | Curated voice catalog per provider |
| `Donna.spec` | PyInstaller bundle spec |
| `build_mac.sh` | One-command macOS build |
| `scripts/download_kokoro_assets.sh` | Fetch Kokoro model for dev/build |

## License

See repository license. Kokoro-82M is [Apache 2.0](https://huggingface.co/hexgrad/Kokoro-82M).
