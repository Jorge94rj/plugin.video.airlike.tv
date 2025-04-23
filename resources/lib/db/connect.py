import xbmc,xbmcaddon,xbmcvfs
import sqlite3

filepath = 'special://profile/addon_data/plugin.video.airlike.tv/airlike.db'
translatedpath = xbmcvfs.translatePath(filepath)

def getDBConn():
  if not xbmcvfs.exists(filepath):
    return
  try:
      conn = sqlite3.connect(translatedpath, detect_types=sqlite3.PARSE_DECLTYPES)
      conn.row_factory = sqlite3.Row
      return conn.cursor()
  except Exception as detail:
      xbmc.log("EXCEPTION: (script.tvguide.fullscreen)  %s" % detail, xbmc.LOGERROR)