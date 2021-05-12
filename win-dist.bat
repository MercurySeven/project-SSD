RMDIR /Q /S build
RMDIR /Q /S dist

ECHO "Copio shiboken6.abi3.dll nella cartella PySide6"
COPY venv\Lib\site-packages\shiboken6\shiboken6.abi3.dll venv\Lib\site-packages\PySide6

CALL "./venv/Scripts/Activate.bat"
pip install -r .\requirements.txt

pyinstaller --name="SSD" --windowed --noconfirm ^
--add-data "./venv/Lib/site-packages/PySide6/plugins;PySide6/plugins/" ^
--add-data "./assets;assets" ^
--specpath "." ^
--hidden-import "PySide6" ^
--icon="assets/icons/logo.ico" ^
--onefile ^
src/__main__.py

DEl SSD.spec

PAUSE