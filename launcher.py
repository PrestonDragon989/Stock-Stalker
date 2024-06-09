import license

from database.start import DatabaseStarter as DBS

from window.root import RootWindow


class Launcher:
    def __init__(self):
        license.ensure()

        self.dbs = DBS()
        self.dbs.start()
        self.database = None

        self.user_data = None

        self.root = RootWindow(self)

    def update_database(self):
        self.database = self.dbs.database()
        return self.database

    def start(self):
        self.root.init_root_data()
        self.root.layout()
        self.root.set_binds()

        return self

    def run(self):
        self.root.launch()

        return self


if __name__ == '__main__':
    lau = Launcher().start().run()
    lau.database.client.close() if lau.database else None
