from graphene import ObjectType, String, Schema, List
from flask_graphql import GraphQLView
from settings import Settings
from typing import Generator
from flask import Flask
import threading
import os


def dir_content(path: str) -> Generator[str, None, None]:
    """returns the contents of the folder"""
    path = os.path.join(Settings['REAL_PATH'], path)
    for root, dirs, files in os.walk(path):
        root = root.replace(path, "")
        for name in dirs + files:
            yield os.path.join(root, name)


class Query(ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    content = List(String, path=String(default_value="defcon1"))
    goodbye = String()

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    def resolve_content(root, info, path):
        return list(dir_content(path))

    def resolve_goodbye(root, info):
        return 'See ya!'


class API_Server:

    def __init__(self, host: str, port: int):

        self.HOST = host
        self.PORT = port
        self.serverd = None

        self.view_func = GraphQLView.as_view(
            'graphql', schema=Schema(query=Query), graphiql=True)

        self.app = Flask(__name__)
        self.app.add_url_rule('/graphql', view_func=self.view_func)

    def daemon(self):
        # start app
        self.app.run(
            host=self.HOST,
            port=os.environ.get('PORT', self.PORT),
            debug=False,
            use_reloader=False
        )

    def run(self):
        if not self.serverd:
            self.serverd = threading.Thread(target=self.daemon, args=())
            self.serverd.setDaemon(True)
            self.serverd.start()
            print("server started")
