import os
import zipfile
from datetime import datetime

files_to_exclude = ['.gitignore', 'Readme.md', '.DS_Store', 'buildrelease.py', 'airlike-plugin.code-workspace']
folders_to_exclude = ['.git', 'tools']

today = datetime.today()

current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
output_dir_name = 'dist'
output_file_name = f"plugin.video.airlike.tv_release-{today.strftime('%Y-%m-%d %H:%M:%S')}.zip"

files_to_exclude.append(output_file_name)

def get_zip_file_name():
    return output_file_name

def get_zip_file_path():
    return f"{output_dir_name}/{output_file_name}"

def create_zip_file():
    # create dist folder if it does not exist
    if not os.path.isdir(output_dir_name):
        os.mkdir(output_dir_name)

    with zipfile.ZipFile(get_zip_file_path(), 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(parent_dir):
            for file in files:
                current_file = os.path.join(root, file)
                should_exclude = False
                for folderToExclude in folders_to_exclude:
                    if folderToExclude in f"/{current_file}":
                        should_exclude = True
                        break
                if not (file in files_to_exclude) and (not should_exclude):
                    # print(f"Writing {file} to {output_file_name}")
                    relative_path = os.path.relpath(current_file, parent_dir)
                    zipf.write(current_file, arcname=relative_path)