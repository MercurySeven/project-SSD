import os
import pathlib

from PySide6.QtCore import QSettings, QCoreApplication

from src import settings


def setUp() -> [str, QSettings]:
    QCoreApplication.setOrganizationName("MercurySeven")
    QCoreApplication.setApplicationName("SSD")
    env_settings = QSettings()
    restore_path = env_settings.value("sync_path")

    path = os.path.join(str(pathlib.Path().absolute()), "tests")
    path = r'%s' % path
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    env_settings.setValue("sync_path", path)
    settings.file_name = os.path.join(path, "config.ini")
    settings.check_file()

    return [restore_path, env_settings]


def tearDown(env_settings: QSettings, restore_path) -> None:
    os.remove(settings.file_name)
    env_settings.setValue("sync_path", restore_path)
