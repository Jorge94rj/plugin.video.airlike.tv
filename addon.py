# Module: main
# Author: Roman V. M.
# Created on: 28.11.2014
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
"""
Example video plugin that is compatible with Kodi 19.x "Matrix" and above
"""
import sys
from urllib.parse import parse_qsl
import xbmc
import xbmcgui
import xbmcaddon
from resources.lib.channelgenerator import list_channels
from resources.lib.contentmanager import getContent, play_video

dialog = xbmcgui.Dialog()
WINDOW = xbmcgui.Window(10000)
PLAYER_WINDOW = xbmcgui.Window(12005)

# Get the plugin url in plugin:// notation.
# Get the plugin handle as an integer number.

# Free sample videos are provided by www.vidsplay.com
# Here we use a fixed set of properties simply for demonstrating purposes
# In a "real life" plugin you will need to get info and links to video files/streams
# from some web-site or online service.

__addon__        = xbmcaddon.Addon()
__setting__      = __addon__.getSetting
keep_logs        = True if __setting__('logging') == 'true' else False

# def onAction(self, action):
#     print('DEBUG_ACTIon', action)
#   if action.getId() == ACTION_PREVIOUS_MENU:
#     print('action received: previous')
#     self.close()
#   if action.getId() == ACTION_SHOW_INFO:
#     print('action received: show info')
#   if action.getId() == ACTION_STOP:
#     print('action received: stop')
#   if action.getId() == ACTION_PAUSE:
#     print('action received: pause')

def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    isPlaying = xbmc.Player().isPlaying()
    hasImageControl = WINDOW.getProperty("airlike.hasImageControl")
    if not isPlaying and hasImageControl:
        ctrl = PLAYER_WINDOW.getControl(int(hasImageControl))
        PLAYER_WINDOW.removeControl(ctrl)
        WINDOW.clearProperty("airlike.hasImageControl")

    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        # if params['action'] == 'listing':
        #     # Display the list of videos in a provided category.
        #     list_videos(params['category'])
        if params['action'] == 'play':
            # Play a video from a provided URL.
            channelId = params['category']
            getContent(channelId)
            play_video()
            WINDOW.setProperty("airlike.tv_current_channel", channelId)
        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {}!'.format(paramstring))
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video channels
        list_channels()


if __name__ == '__main__':
    router(sys.argv[2][1:])
