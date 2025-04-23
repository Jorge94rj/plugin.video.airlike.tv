# Module: main
# Author: Roman V. M.
# Created on: 28.11.2014
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
import sys
import os
from urllib.parse import urlencode
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmcvfs
from datetime import datetime, timedelta
from resources.lib.db.connect import getDBConn
from resources.lib.enums import ChannelKeys

dialog           = xbmcgui.Dialog()
WINDOW           = xbmcgui.Window(10000)

# Get the plugin url in plugin:// notation.
_URL = sys.argv[0]
# Get the plugin handle as an integer number.
_HANDLE = int(sys.argv[1])


__addon__        = xbmcaddon.Addon()
__setting__      = __addon__.getSetting
keep_logs        = True if __setting__('logging') == 'true' else False

addonPath = __addon__.getAddonInfo('path')
addonProfile = __addon__.getAddonInfo('profile')
defaultThumbnail = os.path.join(addonPath, 'resources/images/thumbnail.default.png')
defaultFanart = os.path.join(addonPath, 'resources/images/fanart.default.png')


def get_url(**kwargs):
    return '{}?{}'.format(_URL, urlencode(kwargs))


def list_channels():
    """
    Create the list of video channels in the Kodi interface.
    """
    connection = getDBConn()
    if not connection:
        return
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_HANDLE, 'My Video Collection')
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_HANDLE, 'videos')
    # Get video channels
    connection.execute(
        'SELECT id, name, thumbnail, icon, fanart FROM channel'
    )
    channels = connection.fetchall()
    # Iterate through channels
    for channel in channels:
        # Create a list item with a text label and a thumbnail image.
        channelId = channel[ChannelKeys['id']]
        channelName = channel[ChannelKeys['name']]
        list_item = xbmcgui.ListItem(label=channelName)

        channelThumbnail = f'{addonProfile}media/thumbnail.{channelId}.png'
        if not xbmcvfs.exists(channelThumbnail):
            channelThumbnail = defaultThumbnail

        channelFanart = f'{addonProfile}media/fanart.{channelId}.png'
        if not xbmcvfs.exists(channelFanart):
            channelFanart = defaultFanart

        list_item.setArt({'thumb': channelThumbnail,
                          'icon': channelThumbnail,
                          'fanart': channelFanart})
        
        list_item.setInfo('video', {'title': channelName,
                                    # 'genre': channelName,
                                    'mediatype': 'video'})
        
        url = get_url(action='play', category=channelId)
        is_folder = True
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
        # xbmc.executebuiltin("Container.SetViewMode(500)")
        xbmc.executebuiltin("Container.SetViewMode(500)")
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_HANDLE)
        