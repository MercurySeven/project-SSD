import os
import platform

if platform.system() == 'Windows':
    file_name = "./src/assets"
else:
    dir_name = os.path.dirname(__file__)
    file_name = os.path.join(dir_name, "./assets")

ASSETS_PATH = file_name
