from couchdb import Server


class CouchDBClass:

    def __init__(self, username, password, url, db_name):
        self.server = Server(f"http://{username}:{password}@{url}")
        self.db_name = db_name
        self.db = None
        self.connect()

    def connect(self):
        if self.db_name in self.server:
            self.db = self.server[self.db_name]
        else:
            self.db = self.server.create(self.db_name)

    def insert_data(self, data):
        self.db.save(data)

    def get_data(self):
        pass
