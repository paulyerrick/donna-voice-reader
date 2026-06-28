# -*- mode: python ; coding: utf-8 -*-
import sysconfig
import spacy
from pathlib import Path
from PyInstaller.utils.hooks import collect_all, copy_metadata

target_arch = sysconfig.get_platform().rsplit('-', 1)[-1]

spacy_model = Path(spacy.util.get_package_path('en_core_web_sm'))

datas = [
    ('static', 'static'),
    ('voices.json', '.'),
    ('assets/Donna.icns', 'assets'),
    ('assets/kokoro', 'kokoro'),
    ('kokoro_engine.py', '.'),
]
binaries = []
hiddenimports = [
    'kokoro_engine',
    'kokoro',
    'kokoro.model',
    'kokoro.pipeline',
    'misaki',
    'misaki.en',
    'misaki.espeak',
    'en_core_web_sm',
    'soundfile',
    'spacy',
    'spacy.lang.en',
    'curated_transformers',
    'curated_tokenizers',
    'espeakng_loader',
]

for pkg in (
    'torch', 'kokoro', 'transformers', 'spacy', 'misaki',
    'language_tags', 'phonemizer_fork', 'csvw', 'segments',
    'curated_transformers', 'curated_tokenizers', 'en_core_web_sm',
    'espeakng_loader',
):
    tmp = collect_all(pkg)
    datas += tmp[0]
    binaries += tmp[1]
    hiddenimports += tmp[2]

for meta in ('torch', 'transformers', 'spacy', 'misaki', 'kokoro', 'en_core_web_sm'):
    datas += copy_metadata(meta)

datas += [(str(spacy_model), 'en_core_web_sm')]

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Donna',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=target_arch,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='Donna',
)
app = BUNDLE(
    coll,
    name='Donna.app',
    icon='assets/Donna.icns',
    bundle_identifier='com.donna.voicereader',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'CFBundleShortVersionString': '0.2.0',
        'CFBundleVersion': '0.2.0',
    },
)