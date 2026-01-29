# -*- mode: python ; coding: utf-8 -*-
# Configuración para crear un ejecutable ÚNICO y STANDALONE
# Todo incluido en un solo .exe sin dependencia de carpetas externas

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('RESOURCES', 'RESOURCES'), ('DATA', 'DATA')],
    hiddenimports=['PySide6'],
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
    name='Torneo_Futbol',
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
    onefile=True,  # ← CLAVE: Un único archivo .exe
)
