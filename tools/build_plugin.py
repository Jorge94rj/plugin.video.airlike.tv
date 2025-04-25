from print_color import Color, print_color
from create_zip_file import create_zip_file, get_zip_file_name

output_file_name = get_zip_file_name()

warning_message = '''
Due to an incompatibility between Python's zipfile module and Kodi's plugin installation function, 
the generated ZIP file must be extracted and recompressed using another tool, such as the default 
compression utility provided by your operating system.
'''
print_color(f"Creating zip file [{output_file_name}]", Color.GREEN)
create_zip_file()
print_color(f"[{output_file_name}] has been generated successfully", Color.GREEN)
print_color(warning_message, Color.RED)