from enum import Enum

class Color(Enum):
  GREEN = "\033[32m"
  YELLOW = "\033[33m"
  RED = "\033[91m"
  CYAN = "\033[36m"
  CLEAR = "\033[0m"
  
def print_color(message, color):
  print(f"{color.value}{message}{Color.CLEAR.value}")