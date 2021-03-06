# -*- mode: python ; coding: utf-8 -*-
block_cipher = None


a = Analysis(['src/main.py'],
             pathex=["."],
             binaries=[],
             datas=[
                 ("./venv/Lib/site-packages/PySide6/plugins", "PySide6/plugins/"),
                 ("./assets", "assets")],
             hiddenimports=["PySide6"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Zextras Drive Desktop',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Zextras Drive Desktop')