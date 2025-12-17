import os
import json
import zipfile
import shutil

from create_zip_file import create_zip_file, get_zip_file_path

def copy_plugin():
    with open('settings.json', 'r') as file:
        settings = json.load(file)

    if not settings['destination']:
        print('destination prop must be set in settings.json file')
        return
    
    create_zip_file(nest_content=False)
    
    source_dir = get_zip_file_path()
    destination_dir = settings['destination']

    # if destination dir exists, remove it
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)

    # extract zip file and copy the content to the destionation dir
    with zipfile.ZipFile(source_dir, 'r') as zip_ref:
        zip_ref.extractall(destination_dir)

copy_plugin()
