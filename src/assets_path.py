import os
__DEPLOY_MACOS = False

if __DEPLOY_MACOS:
    dir_name = os.path.dirname(__file__)
    file_name = os.path.join(dir_name, "./assets")
    ASSETS_PATH = file_name
else:
    ASSETS_PATH = "./src/assets"
