import os
import sys

import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs

import json
import shutil

__addon__        = xbmcaddon.Addon('plugin.video.airlike.tv')
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
addonProfile = __addon__.getAddonInfo('profile')
supportedMedia = xbmc.getSupportedMedia('video')
profilePath = xbmcvfs.translatePath(addonProfile)
settingsFile = f'{profilePath}settings.json'
time = 5000 #in miliseconds
dialog = xbmcgui.Dialog()


def getSettings():
  try:
    with open(settingsFile) as json_file:
      return json.load(json_file)
  except:
    dialog.ok('Warning', 'In order to play content you need to set parent directory')
    sys.exit(0)

def setParentDir():
  selectedpath = dialog.browse(0, 'Select directory','files','',False,False)
  data = {
    'parentDir': selectedpath
  }
  with open(settingsFile, 'w+') as outfile:
    json.dump(data, outfile)

def importMediaFolder():
  mediapath = f'{addonProfile}/media'
  if not xbmcvfs.exists(mediapath):
    xbmcvfs.mkdirs(mediapath)
  selectedfile = dialog.browse(1, 'Select media zip','files','',False,False)
  shutil.unpack_archive(selectedfile, f'{profilePath}/media')

def importDB():
  if not xbmcvfs.exists(addonProfile):
    xbmcvfs.mkdirs(addonProfile)
  selectedfile = dialog.browse(1, 'Select db file','files','',False,False)
  xbmcvfs.copy(selectedfile, f'{addonProfile}airlike.db')

def showNotification(message):
  xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,message, time, __icon__))