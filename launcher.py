import license

from database.start import DatabaseStarter as DBS

import stocks.client as sc

from window.root import RootWindow


class Launcher:
    def __init__(self):
        self.version = "1.0.0"

        self.name = "STALKER"

        print(f"Welcome to {self.name}! Sorry that you have to use the seen console edition, but it can't be helped.")

        license.ensure()

        self.dbs = DBS(self.name)
        self.dbs.start()
        self.database = None

        self.user_data = None
        self.user_stock = None

        self.stock_client = sc

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
