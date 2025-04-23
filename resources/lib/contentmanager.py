import os
import sys

import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs

from datetime import datetime, timedelta

__addon__ = xbmcaddon.Addon('plugin.video.airlike.tv')
addonPath = __addon__.getAddonInfo('path')
addonProfile = __addon__.getAddonInfo('profile')
sys.path.append(addonPath)

from resources.lib.enums import BlockKeys
from resources.lib.db.connect import getDBConn
from resources.lib.db.debug_updatedb import applyUpdate
from resources.lib.utils import getSettings

WINDOW = xbmcgui.Window(10000)
PLAYER_WINDOW = xbmcgui.Window(12005)
player = xbmc.Player()
playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
imageCtrl = xbmcgui.ControlImage(1556, 64, 128, 128, 'None', aspectRatio=2)
imageCtrl.setColorDiffuse('0x80FFFFFF')

currentStreamProgress = 0
totalDuration = 0
lastDuration = 0
lastBlockPlayed = 0
staticVideo = os.path.join(addonPath, 'resources/static.mp4')
defaultLogo = os.path.join(addonPath, 'resources/images/thumbnail.default.png')
channelLogo = defaultLogo
dt = datetime.now()
day = dt.weekday()

parentDir = None

currentHour = f"'{dt.strftime('%H:%M')}'"
from1 = 'TIME(%s) >= TIME(b.start_time)' % (currentHour)
to1 = 'TIME(%s) <= TIME(b.start_time,"+1 hours")' % (currentHour)
from2 = 'TIME(%s) <= TIME(b.start_time)' % (currentHour)
to2 = 'TIME(b.start_time) < TIME(%s,"+1 hours")' % (currentHour)

#DEBUG STUFF ID RANGE IS 1 - 7
updateDB = True
updateDayTo = 7
updateStartTimeTo = '14:20'

def updateContent(channelId):
    global parentDir
    
    try:
        connection = getDBConn()
        if not connection:
            return

        parentDir = getSettings()['parentDir']
        blocks = getAvailableBlocks(channelId)
        createBlocks(blocks)

    except Exception as e:
        print("DEBUG_failed to update list properly on updating", e)
        return


def getContent(channelId):
    global parentDir

    try:
        getChannelLogo(channelId)
        updatePlayedMedia(channelId)
        parentDir = getSettings()['parentDir']
        blocks = getAvailableBlocks(channelId)
        createBlocks(blocks)
    except Exception as e:
        print("DEBUG_failed to update list properly", e)
        return

def updatePlayedMedia(channelId):
    connection = getDBConn()
    if not connection:
        return
    
    # check if all content is played, if so reset it to 0
    connection.execute(
        'SELECT m.content_id, COUNT(played) as total, SUM(played) as played FROM channel_day_block cdb' + ' '
        'INNER JOIN channel_day cd ON cdb.channel_day_id = cd.id' + ' '
        'INNER JOIN channel c ON cd.channel_id = c.id' + ' '
        'INNER JOIN day d ON cd.day_id = d.id' + ' '
        'INNER JOIN block b ON cdb.block_id = b.id' + ' '
        'INNER JOIN media m ON b.content_id = m.content_id' + ' '
        'WHERE c.id=%s AND d.day=%s' % (channelId,day) + ' '
        'GROUP BY m.content_id'
    )

    media = connection.fetchall()

    for item in media:
        contentId = item['content_id']
        total = item['total']
        played = item['played']
        if played >= total:
            connection.execute('UPDATE media SET played=0, last_date_played=NULL WHERE content_id = "%s"' % contentId)
            connection.connection.commit()

    # update played status
    now = f'{dt.now().strftime("%Y-%m-%d")} 00:00:00'
    # now = '2023-01-28 10:47:43'
    connection.execute('UPDATE media SET played=1 WHERE last_date_played < "%s"' % now)
    connection.connection.commit()


def play_video():
    if playlist.size() > 0:
        player.play(playlist)
        xbmc.executebuiltin('PlayerControl(repeatOff)')
        xbmc.sleep(1000)
        if player.isPlaying():
            xbmc.sleep(1000)
            player.playselected(0)
            player.seekTime(currentStreamProgress)
            showChannelLogo()
    else:
        player.play(staticVideo)
        xbmc.executebuiltin('PlayerControl(repeat)')

def getChannelLogo(channelId):
    global channelLogo

    hasImageControl = WINDOW.getProperty("airlike.hasImageControl")

    if not hasImageControl:
        PLAYER_WINDOW.addControl(imageCtrl)
        WINDOW.setProperty("airlike.hasImageControl", str(imageCtrl.getId()))

    imageCtrl.setImage('None')

    resource = f'{addonProfile}media/thumbnail.{channelId}.png'
    if xbmcvfs.exists(resource):
        channelLogo = resource


def showChannelLogo():
    imageCtrl.setImage(channelLogo)


def getAvailableBlocks(channelId):
    connection = getDBConn()
    if not connection:
        return
    # DEBUG_STUFF
    # if updateDB:
    #     applyUpdate(connection, updateDayTo, updateStartTimeTo)
    #     xbmc.sleep(1000)
    #     connection.connection.commit()

    connection.execute(
        'SELECT cdb.block_id, c.name, thumbnail, start_time, len' + ' '
        'FROM channel_day_block cdb INNER JOIN channel_day cd ON cdb.channel_day_id = cd.id' + ' '
        'INNER JOIN channel c ON cd.channel_id = c.id' + ' '
        'INNER JOIN day d ON cd.day_id = d.id' + ' '
        'INNER JOIN block b ON cdb.block_id = b.id' + ' '
        'WHERE c.id=%s AND d.day=%s' % (channelId,day) + ' '
        'AND ((%s AND %s) OR (%s AND %s))' % (from1, to1, from2, to2)
    )

    return connection.fetchall()


def createBlocks(blocks):
    global currentStreamProgress
    global lastBlockPlayed

    playlist.clear()

    if len(blocks) == 0:
        return

    startTimeParsed = blocks[0][BlockKeys['start_time']].split(':')
    lastBlockPlayed = dt.replace(hour=int(startTimeParsed[0]), minute=int(startTimeParsed[1]))

    for block in blocks:
        createBlock(block)

    connection = getDBConn()
    
    if not connection:
        return

    playedTime = (dt - timedelta(hours=lastBlockPlayed.hour,minutes=lastBlockPlayed.minute)).minute

    if totalDuration < playedTime:
        currentStreamProgress =  abs(totalDuration - playedTime) * 60
    else:
        currentStreamProgress = (playedTime - lastDuration) * 60


def createBlock(block):
    global currentStreamProgress
    global totalDuration
    global lastBlockPlayed
    global lastDuration

    blockId = block[BlockKeys['block_id']]
    startTimeParsed = block[BlockKeys['start_time']].split(':')
    len = block[BlockKeys['len']]
    startTime = dt.replace(hour=int(startTimeParsed[0]), minute=int(startTimeParsed[1]))
    connection = getDBConn()
    if not connection:
        return

    connection.execute(
        'SELECT m.id,path,filename,duration FROM channel_day_block cdb' + ' '
        'INNER JOIN  block b ON cdb.block_id = b.id' + ' '
        'INNER JOIN media m ON b.content_id = m.content_id' + ' '
        'WHERE cdb.block_id=%s AND played=0 LIMIT %s' 
        % (blockId,len)
    )
    mediaItems = connection.fetchall()
    # update played media

    totalDuration = 0

    for item in mediaItems:
        duration = item['duration']
        totalDuration += duration
        if dt <= (dt.replace(hour=startTime.hour,minute=startTime.minute) + timedelta(minutes=totalDuration)):
            addItemToPlaylist(item['path'], item['filename'])
            now = dt.now().strftime("%Y-%m-%d %H:%M:%S")
            # datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            # TESTED datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
            connection.execute('UPDATE media SET last_date_played="%s" WHERE filename="%s"' % (now, item['filename']))
            connection.connection.commit()
        else:
            lastDuration = duration
            lastBlockPlayed = startTime


def addItemToPlaylist(path, file):
    filepath = parentDir+path+file
    listitem = xbmcgui.ListItem(file)
    playlist.add(url=filepath, listitem=listitem)


if __name__ == '__main__':
    channelId = WINDOW.getProperty("airlike.tv_current_channel")
    if player.isPlaying() and channelId:
        updateContent(channelId)
