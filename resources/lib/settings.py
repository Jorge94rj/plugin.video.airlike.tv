import sys
from utils import setParentDir, importDB, importMediaFolder

def entry(args):
  command = args[1]
  if command == 'Dir':
    setParentDir()
  elif command == 'Db':
    importDB()
  elif command == 'Media':
    importMediaFolder()
    
  

if __name__ == '__main__': entry(sys.argv)