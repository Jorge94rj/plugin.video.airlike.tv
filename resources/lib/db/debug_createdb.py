import xbmc,xbmcaddon
import sqlite3

path = '/Users/jorgereyes/Desktop/test.db'
#TEST VALUES
startBlock1 = '22:00'
startBlock2 = '23:40'

def createDB():
  try:
      conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
      cursor = conn.cursor()
      createTables(cursor)
      seedTables(cursor)
      conn.commit()
    #   cursor.close()
  except Exception as detail:
      xbmc.log("EXCEPTION: (script.tvguide.fullscreen)  %s" % detail, xbmc.LOGERROR)

def createTables(cursor):
    cursor.execute(
      'CREATE TABLE channel('
      +'id INTEGER PRIMARY KEY,'
      +'name TEXT,'
      +'thumbnail TEXT,'
      +'icon TEXT,'
      +'fanart TEXT'
      +')')
      
    cursor.execute(
      'CREATE TABLE day('
      +'id INTEGER PRIMARY KEY,'
      +'day INTEGER,'
      +'channel_id INTEGER,'
      +'FOREIGN KEY (channel_id)'
      +'REFERENCES channel (channel_id)'
      +')')

    cursor.execute(
      'CREATE TABLE block('
      +'id INTEGER PRIMARY KEY,'
      +'day_id INTEGER,'
      +'start_time TEXT,'
      # +'path TEXT,'
      +'len INTEGER,'
      +'last_idx_played INTEGER,'
      +'FOREIGN KEY (day_id)'
      +'REFERENCES day (day_id)'
      +')')

    cursor.execute(
      'CREATE TABLE media('
      +'id INTEGER PRIMARY KEY,'
      +'block_id INTEGER,'
      +'path TEXT,'
      +'filename TEXT,'
      +'duration INTEGER,'
      +'played INTEGER,'
      +'FOREIGN KEY (block_id)'
      +'REFERENCES block (block_id)'
      +')')

def seedTables(cursor):
    cursor.execute('INSERT INTO channel(name,thumbnail,icon,fanart) VALUES (?,?,?,?)', 
    [
      'Test Channel',
      'https://companieslogo.com/img/orig/WBD_BIG-57ba1b48.png?t=1649700090',
      'https://companieslogo.com/img/orig/WBD_BIG-57ba1b48.png?t=1649700090',
      'https://i.redd.it/h5fhtwt3mt991.png'
    ])
    cursor.execute('INSERT INTO day(day,channel_id) VALUES (?,?)', 
    [
      0,
      1
    ])
    cursor.execute('INSERT INTO day(day,channel_id) VALUES (?,?)', 
    [
      1,
      1
    ])
    cursor.execute('INSERT INTO day(day,channel_id) VALUES (?,?)', 
    [
      2,
      1
    ])
    cursor.execute('INSERT INTO day(day,channel_id) VALUES (?,?)', 
    [
      3,
      1
    ])
    cursor.execute('INSERT INTO day(day,channel_id) VALUES (?,?)', 
    [
      4,
      1
    ])
    cursor.execute('INSERT INTO day(day,channel_id) VALUES (?,?)', 
    [
      5,
      1
    ])
    cursor.execute('INSERT INTO day(day,channel_id) VALUES (?,?)', 
    [
      6,
      1
    ])
    cursor.execute('INSERT INTO block(day_id,start_time,path,len,last_idx_played) VALUES (?,?,?,?,?)', 
    [
      6,
      startBlock1,
      '/Users/jorgereyes/Desktop/ktest/SPY×FAMILY (2022)/',
      2,
      -1
    ])
    cursor.execute('INSERT INTO block(day_id,start_time,path,len,last_idx_played) VALUES (?,?,?,?,?)', 
    [
      6,
      startBlock2,
      '/Users/jorgereyes/Desktop/ktest/Elfen Lied (2004)/',
      2,
      -1
    ])
    cursor.execute('INSERT INTO media(block_id,filename,duration,played) VALUES (?,?,?,?)', 
    [
      1,
      'SPY×FAMILY (2022) S01E21.mp4',
      24,
      0
    ])
    cursor.execute('INSERT INTO media(block_id,filename,duration,played) VALUES (?,?,?,?)', 
    [
      1,
      'SPY×FAMILY (2022) S01E22.mp4',
      24,
      0
    ])
    cursor.execute('INSERT INTO media(block_id,filename,duration,played) VALUES (?,?,?,?)', 
    [
      2,
      'Elfen Lied (2004) S01E01.mp4',
      25,
      0
    ])
    cursor.execute('INSERT INTO media(block_id,filename,duration,played) VALUES (?,?,?,?)', 
    [
      2,
      'Elfen Lied (2004) S01E02.mp4',
      25,
      0
    ])
    # data = [
    #     ("/Users/jorgereyes/Desktop/item1"),
    #     ("/Users/jorgereyes/Desktop/item2"),
    #     ("/Users/jorgereyes/Desktop/item3"),
    # ]
    # cursor.executemany('INSERT INTO channel(thumbnail) VALUES (?)', data)
