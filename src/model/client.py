from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


class API_Client():

    def __init__(self, host: str, port: int):

        self.HOST = host  # server hostname or IP address
        self.PORT = port  # server port
    
    def get_content(self, query: str):
        transport = RequestsHTTPTransport(
            url=f"http://{self.HOST}:{self.PORT}/graphql",
            use_json=True,
            headers={
                "Content-type": "application/json",
                "Accept-Encoding": "gzip"
            },
            verify=False,
            retries=3
        )
        client = Client(transport=transport, fetch_schema_from_transport=False)

        return client.execute(gql(query))