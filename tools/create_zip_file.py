import os
import zipfile
from datetime import datetime
from print_color import Color, print_color

plugin_name = "plugin.video.airlike.tv"

plugin_content = [
    {"name": "addon.py", "is_dir": False},
    {"name": "addon.xml", "is_dir": False},
    {"name": "setcron.py", "is_dir": False},
    {"name": "resources", "is_dir": True},
]

today = datetime.today()

current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
output_dir_name = 'dist'
output_file_name = f"{plugin_name}_release-{today.strftime('%Y-%m-%d')}T{today.strftime('%H%M%S')}Z.zip"

def get_zip_file_name():
    return output_file_name

def get_zip_file_path():
    return f"{output_dir_name}/{output_file_name}"

def create_zip_file(nest_content = True):
    # create dist folder if it does not exist
    if not os.path.isdir(output_dir_name):
        os.mkdir(output_dir_name)

    with zipfile.ZipFile(get_zip_file_path(), 'w') as zipf:
        for content in plugin_content:
            content_path = f"{parent_dir}/{content['name']}"
            if content["is_dir"]:
                write_dir(content_path, zipf, nest_content)
            else:
                relative_path = os.path.relpath(content_path, parent_dir)
                nested_path = os.path.join(plugin_name, relative_path)
                final_path = nested_path if nest_content == True else relative_path
                zipf.write(content_path, arcname=final_path)
        
        print_color(f"Content in [{output_file_name}]", Color.CYAN)
        for name in zipf.namelist():
            print_color(name, Color.YELLOW)
        zipf.close()

def write_dir(dir_name, zipf, nest_content):
    for root, _, files in os.walk(dir_name):
            for file in files:
                if file == '.DS_Store':
                    continue
                current_file = os.path.join(root, file)
                relative_path = os.path.relpath(current_file, parent_dir)
                nested_path = os.path.join(plugin_name, relative_path)
                final_path = nested_path if nest_content == True else relative_path
                zipf.write(current_file, arcname=final_path)