def applyUpdate(conn,day,startTime):
  strTime = f"'{startTime}'"
  conn.execute('UPDATE block SET day_id=%s WHERE block.id=1' % (day))
  conn.execute('UPDATE block SET start_time=%s WHERE block.id=1' % (strTime))
  conn.execute('UPDATE block SET day_id=%s WHERE block.id=2' % (day))
  conn.execute('UPDATE block SET start_time = CAST(TIME(%s,"+48 minutes") AS VARCHAR) WHERE block.id=2' % (strTime))
  # print('DEBUG_query','UPDATE block SET start_time=%s WHERE block.id=1' % (strTime))
  