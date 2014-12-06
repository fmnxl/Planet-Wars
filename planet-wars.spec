# -*- mode: python -*-
a = Analysis(['planet-wars.py'],
             pathex=['/Users/freemanlatif/Documents/Masters/G54PRG/game'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='planet-wars',
          debug=True,
          strip=None,
          upx=True,
          console=True )


sound_tree = Tree('sound', prefix = 'sound')
img_tree = Tree('img', prefix = 'img')
font_tree = Tree('font', prefix = 'font')
coll = COLLECT(exe,
               a.binaries,
               sound_tree,
               img_tree,
               font_tree,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='planet-wars')
