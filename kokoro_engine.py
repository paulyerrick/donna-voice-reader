"""Bundled Kokoro-82M local TTS engine."""

import os
import io
import threading
import numpy as np

_pipeline = None
_voice_dir = None
_init_lock = threading.Lock()
SAMPLE_RATE = 24000

VOICE_FILES = {
    "af_heart": "af_heart.pt",
    "af_bella": "af_bella.pt",
    "am_adam": "am_adam.pt",
    "am_michael": "am_michael.pt",
    "bf_emma": "bf_emma.pt",
}


def resolve_kokoro_dir(app_root):
    bundled = os.path.join(app_root, "kokoro")
    if os.path.isfile(os.path.join(bundled, "kokoro-v1_0.pth")):
        return bundled
    dev = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "kokoro")
    if os.path.isfile(os.path.join(dev, "kokoro-v1_0.pth")):
        return dev
    raise FileNotFoundError(
        "Kokoro model files not found. Run scripts/download_kokoro_assets.sh before building."
    )


def _audio_to_wav(audio):
    import soundfile as sf

    audio = np.asarray(audio, dtype=np.float32)
    if audio.size == 0:
        raise ValueError("Kokoro produced no audio for this text.")
    peak = np.max(np.abs(audio))
    if peak > 1.0:
        audio = audio / peak

    buf = io.BytesIO()
    sf.write(buf, audio, SAMPLE_RATE, format="WAV", subtype="PCM_16")
    buf.seek(0)
    return buf.read()


def get_pipeline(app_root):
    global _pipeline, _voice_dir
    with _init_lock:
        if _pipeline is not None:
            return _pipeline

        os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

        import torch
        from kokoro import KPipeline
        from kokoro.model import KModel

        kokoro_dir = resolve_kokoro_dir(app_root)
        config_path = os.path.join(kokoro_dir, "config.json")
        model_path = os.path.join(kokoro_dir, "kokoro-v1_0.pth")
        _voice_dir = os.path.join(kokoro_dir, "voices")

        if torch.cuda.is_available():
            device = "cuda"
        else:
            # Kokoro's ISTFT path uses complex dtypes that MPS does not support reliably.
            device = "cpu"

        kmodel = KModel(
            repo_id="hexgrad/Kokoro-82M",
            config=config_path,
            model=model_path,
        ).to(device).eval()
        _pipeline = KPipeline(
            lang_code="a",
            repo_id="hexgrad/Kokoro-82M",
            model=kmodel,
            device=device,
        )
        return _pipeline


def synthesize(text, voice_id, app_root):
    if voice_id not in VOICE_FILES:
        voice_id = "af_heart"
    pipeline = get_pipeline(app_root)
    voice_path = os.path.join(_voice_dir or "", VOICE_FILES[voice_id])
    chunks = list(pipeline(text, voice=voice_path))
    if not chunks:
        raise ValueError("Kokoro produced no audio for this text.")
    audio = np.concatenate([chunk[2] for chunk in chunks if chunk[2] is not None])
    return _audio_to_wav(audio)
