from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from settings import Settings


class Server:

    def __init__(self):
        self.settings = Settings()
        self.url: str = self.settings.get_server_url()

        transport = AIOHTTPTransport(url=self.url)
        self.client: Client = Client(transport=transport)

    def sendToServer(self, filePath: str, lastUpdate: str) -> None:
        """Richiede il percorso del file e l'orario di ultima modifica"""
        query = gql('''
                mutation SingleUpload($file: Upload!, $datetime: String!) {
                    singleUpload(file: $file, datetime: $datetime) {
                        filename
                        mimetype
                        encoding
                    }
                }
                ''')

        with open(filePath, "rb") as f:
            params = {
                "file": f,
                "datetime": lastUpdate
            }

            result = self.client.execute(
                query, variable_values=params, upload_files=True
            )

            print(result)

    def getAllFiles(self) -> dict[str, str]:
        """Restituisce il nome dei file con l'ultima modifica"""
        query = gql('''
                query {
                    GetAllFiles {
                        Nome
                        DataUltimaModifica
                    }
                }
                ''')
        response = self.client.execute(query)["GetAllFiles"]
        result: dict[str, str] = {}
        for items in response:
            result[items["Nome"]] = items["DataUltimaModifica"]

        return result

    def removeFileByName(self, fileName: str) -> None:
        """Rimuove il file dal cloud"""
        query = gql('''
                mutation RemoveFile($fileName: String!) {
                    removeFile(fileName: $fileName) {
                        Nome
                        DataUltimaModifica
                    }
                }
                ''')

        params = {
            "fileName": fileName
        }

        result = self.client.execute(query, variable_values=params)

        print(result)
