from src.model.files_model import FilesModel
from src.view.file_view import FileView


class FileController:
    def __init__(self, model: FilesModel, view: FileView):
        self._model = model
        self._view = view
        self._model.Sg_model_changed.connect(self._view.Sl_model_changed)
        self._view.refresh_button.clicked.connect(self._model.Sl_update_model)
        self._view.show_path_button.clicked.connect(self._view.Sl_show_path_button_clicked)
