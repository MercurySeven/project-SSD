from PySide6.QtCore import (QObject, Signal, QSettings)


class SetPathModel(QObject):

    Sg_model_changed = Signal()

    def __init__(self):
        super(SetPathModel, self).__init__(None)
        self.env_settings = QSettings()

    def get_path(self) -> str:
        return self.env_settings.value("sync_path")

    def set_path(self, new_path: str) -> None:
        self.env_settings.setValue("sync_path", new_path)
        self.env_settings.sync()
        self.Sg_model_changed.emit()
