# build_plugin.py
This script creates a zip file that can be installed in Kodi

# copy_plugin_to_kodi.py
This script copies the plugin's content to the Kodi/addons installation folder and it's intended to be used for dev purposes.
With this method, the latest changes in code/resources will be reflected in Kodi, avoiding to unistall and then re install the
plugin. Note: you must install the plugin in Kodi through "Install from zip file" the first time you use the plugin
Prerequisites
-set the Kodi/addons installation directory in destination prop in settings.json