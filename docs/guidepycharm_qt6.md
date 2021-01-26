DANIELE GIACHETTO INSTALLAZIONE GUIDATA PYCHARM E QT6


== EFFETTUARE REGISTRAZIONE SU JETBRAINS.COM CON LICENZA STUDENTE==

(Se non si effettua allora scaricare la versione pycharm-community)

# Installazione Pycharm
```
sudo snap install pycharm-professional --classic
cd /snap/pycharm-professional/current/bin
./pycharm.sh
```

## Pycharm dovrebbe avviarsi correttamente

# Setup qt6

## APRIRE PYCHARM (se lo avete chiuso)
```
cd /snap/pycharm-professional/current/bin
./pycharm.sh
```

## SETUP PROGETTO

seguire la procedura guidata di pycharm per creare un nuovo progetto
(o prenderlo dal vcs).

creando un ambiente virtuale dovremmo reinstallare tutte le librerie 
(consiglio un ambiente virtuale isolato per evitare
di avere roba che non serve)

## installazione librerie di base

andare in basso a sinistra e premere su terminal.
inserire 

pip install pyside6

ora copiamo questo codice e facciamolo runnare, dovrebbe funzionare!

```

import sys
import random
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget)
from PySide6.QtCore import Slot, Qt

class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.hello = ["Hallo Welt", "你好，世界", "Hei maailma",
            "Hola Mundo", "Привет мир"]

        self.button = QPushButton("Click me!")
        self.text = QLabel("Hello World")
        self.text.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        # Connecting the signal
        self.button.clicked.connect(self.magic)

    @Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())
``` 

il programma di prova dovrebbe far comparire una gui!

se da problemi con una libreria mancante, ad esempio

``` 

ImportError: libOpenGL.so.0: 
cannot open shared object file: No such file or directory

``` 

per fixare (da terminale esterno a pycharm)
```
sudo apt install libopengl0
```

# Installazione Plugin vari



Tramite il marketplace di pycharm dove installare plugin.

Il marketplace si trova o nella home (con nessun progetto aperta oppure File->Plugins)

## Save actions

Trovate nel marketplace save action (https://plugins.jetbrains.com/plugin/7642-save-actions)
Riavviate l'ide e andate su File->Settings->Other Settings->Save Actions

Attivate la prima spunta ("Activate save actions on save") oppure la spunta del salvataggio con shortcut, a vostro piacimento
Attivate Optimize imports
Poi attivate reformat only changed code


## Autopep8

Per installare autopep8 andate nel terminale ed eseguite 

```
pip install autopep8

```

Dopo seguite questa guida dal punto 1.

https://github.com/hscgavin/autopep8-on-pycharm

Al posto di output filter voi andrete su advanced options.

Per poi runnare autopep8 dovrete per il momento fare tasto destro nel file-> external tools-> autopep8

## Flake8

```
pip install flake8
```

seguire questa guida per impostare mettendo come working directory una cartella con il main (quindi es venv->ciao->main.py)
https://gist.github.com/tossmilestone/23139d870841a3d5cba2aea28da1a895
