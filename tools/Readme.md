# build_plugin.py
This script creates a zip file ~~that can be installed in Kodi~~
Warning: after debugging this tools it was noticed that due to an incompatibility between Python's zipfile module and Kodi's plugin installation function, 
the generated zip file must be extracted and recompressed using another tool, such as the default compression utility provided by your operating system.

# copy_plugin_to_kodi.py
This script copies the plugin's content to the Kodi/addons installation folder and it's intended to be used for dev purposes.
With this method, the latest changes in the code will be reflected in Kodi, avoiding to unistall and then re install the
plugin. Note: you must install the plugin in Kodi through "Install from zip file" the first time you use the plugin
Prerequisites
-set the Kodi/addons installation directory in destination prop in settings.json