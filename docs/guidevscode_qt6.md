# Sviluppare usando VSCode

Passi da seguire:
1. `pip install virtualenv`
2. Windows: `virtualenv venv`  
   Linux: `python3 -m venv venv`
3. Assicuratevi che in basso a sinistra ci sia selezionato Python 3.9.1 64-bit ('venv')
4. Controllate che nel terminale ci sia scritto (venv), altrimenti createne uno da VSCode, cliccando sul +
4. `pip install -r requirements.txt`
5. Create la cartella `.vscode` con all'interno il file `settings.json`
6. Il file dovrà avere il seguente contenuto:
```json
{
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.linting.enabled": true,
    "python.pythonPath": "venv\\Scripts\\python.exe",
    // "python.pythonPath": "venv/bin/python.exe",
    "python.linting.lintOnSave": true,
    "python.testing.pytestPath": "test",
    "python.testing.unittestArgs": [
        "-v",
        "-s",
        ".",
        "-p",
        "*_test.py"
    ],
    "python.testing.pytestEnabled": false,
    "python.testing.nosetestsEnabled": false,
    "python.testing.unittestEnabled": true,
    "files.exclude": {
        "**/__pycache__": true
    }
}
```
7. Crea dentro la cartella `.vscode` il file  `launch.json`, con questo contenuto:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: From main",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/src/__main__.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${cwd}"
            }
        }
    ]
}
```
8. Per generare l'eseguibile: `pyinstaller .\app_inst.spec --noconfirm`