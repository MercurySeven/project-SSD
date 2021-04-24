from abc import ABC, abstractmethod


class Api(ABC):
    @abstractmethod
    def login(self, username: str, password: str):
        pass

    @abstractmethod
    def is_logged(self) -> bool:
        pass

    @abstractmethod
    def get_info_from_email(self):
        pass

    @abstractmethod
    def get_user_id(self):
        pass

    @abstractmethod
    def logout(self):
        pass

    @abstractmethod
    def upload_node(self):
        pass

    @abstractmethod
    def download_node(self):
        pass

    @abstractmethod
    def delete_node(self):
        pass

    @abstractmethod
    def get_content_from_node(self):
        pass

    @abstractmethod
    def create_folder(self):
        pass
