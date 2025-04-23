import xbmcvfs,xbmcgui

path = 'special://profile/addon_data/plugin.video.airlike.tv/'

def importDB():
  if not xbmcvfs.exists(path):
    xbmcvfs.mkdirs(path)
  xbmcvfs.copy('/Users/jorgereyes/Desktop/test.db', f'{path}airlike.db')
