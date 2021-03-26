import html

from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import (QHBoxLayout, QWidget)

from src.model.diff_model import DiffModel
from src.view.widgets.text_edit_number_widget import TextEditNumber
from src.model.difflibparser import DiffCode


class DiffView(QWidget):

    def __init__(self, model: DiffModel, parent=None):

        super(DiffView, self).__init__(parent)
        self.model = model

        # layouts
        # Grid di struttura dell'applicazione
        self.mainGrid = QHBoxLayout(self)
        self.mainGrid.setContentsMargins(0, 0, 0, 0)

        self.text_left = TextEditNumber()
        self.text_right = TextEditNumber()
        self.text_left.setReadOnly(True)
        self.text_right.setReadOnly(True)
        self.show_diff()
        # Imposto il cursore in alto
        cursor = self.text_left.textCursor()
        cursor.movePosition(QTextCursor.Start)
        self.text_left.setTextCursor(cursor)
        cursor = self.text_right.textCursor()
        cursor.movePosition(QTextCursor.Start)
        self.text_right.setTextCursor(cursor)

        self.mainGrid.addWidget(self.text_left)
        self.mainGrid.addWidget(self.text_right)

        self.setLayout(self.mainGrid)

    def return_formatted_line(self, text: str, color: str) -> str:
        text = html.escape(text)
        return f"<span style=\"background-color:{color}\">{text}</span>"

    def line_gray(self, size: int) -> str:
        return f"<pre><span style=\"background-color:#dddddd\">{' ' * size}</span></pre>"

    def show_diff(self):
        redColor = '#ffc4c4'
        darkredColor = '#ff8282'
        greenColor = '#c9fcd6'
        darkgreenColor = '#50c96e'

        for line in self.model.getDiff():
            if line['code'] == DiffCode.SIMILAR:
                self.text_left.appendHtml("<pre>" + html.escape(line['line']) + "</pre>")
                self.text_right.appendHtml("<pre>" + html.escape(line['line']) + "</pre>")
            elif line['code'] == DiffCode.RIGHTONLY:
                self.text_left.appendHtml(self.line_gray(len(line['line'])))
                self.text_right.appendHtml(
                    "<pre>" + self.return_formatted_line(line['line'], greenColor) + "</pre>")
            elif line['code'] == DiffCode.LEFTONLY:
                self.text_left.appendHtml(
                    "<pre>" + self.return_formatted_line(line['line'], redColor) + "</pre>")
                self.text_right.appendHtml(self.line_gray(len(line['line'])))
            elif line['code'] == DiffCode.CHANGED:
                temp_left = ""
                temp_right = ""
                for (i, c) in enumerate(line['line']):
                    color = darkredColor if i in line['leftchanges'] else redColor
                    temp_left = temp_left + self.return_formatted_line(c, color)
                for (i, c) in enumerate(line['newline']):
                    color = darkgreenColor if i in line['rightchanges'] else greenColor
                    temp_right = temp_right + self.return_formatted_line(c, color)
                self.text_left.appendHtml("<pre>" + temp_left + "</pre>")
                self.text_right.appendHtml("<pre>" + temp_right + "</pre>")
