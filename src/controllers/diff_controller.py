from src.model.diff_model import DiffModel
from src.view.diff_view import DiffView


class DiffController:
    def __init__(self, model: DiffModel, view: DiffView):
        self.model = model
        self.view = view

        self.view.text_right.verticalScrollBar().valueChanged.connect(
            self.view.text_left.verticalScrollBar().setValue)
        self.view.text_left.verticalScrollBar().valueChanged.connect(
            self.view.text_right.verticalScrollBar().setValue)
        self.view.text_right.horizontalScrollBar().valueChanged.connect(
            self.view.text_left.horizontalScrollBar().setValue)
        self.view.text_left.horizontalScrollBar().valueChanged.connect(
            self.view.text_right.horizontalScrollBar().setValue)
