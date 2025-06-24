# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['H:\\githubProject\\Augment-free\\src\\augment_free\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('H:\\githubProject\\Augment-free\\src\\augment_free\\web', 'web'), ('H:\\githubProject\\Augment-free\\app.ico', '.')],
    hiddenimports=['pywebview', 'jinja2', 'bottle', 'cffi', 'clr-loader', 'markupsafe', 'proxy-tools', 'pycparser', 'pythonnet', 'typing-extensions', 'webview', 'webview.platforms.winforms', 'webview.platforms.cef', 'webview.platforms.edgechromium', 'bottle', 'jinja2', 'augment_free', 'augment_free.api', 'augment_free.api.core', 'augment_free.api.handlers', 'augment_free.api.handlers.database', 'augment_free.api.handlers.telemetry', 'augment_free.api.handlers.workspace', 'augment_free.utils', 'augment_free.utils.device_codes', 'augment_free.utils.paths'],
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
    a.binaries,
    a.datas,
    [],
    name='AugmentFree',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['H:\\githubProject\\Augment-free\\app.ico'],
)
