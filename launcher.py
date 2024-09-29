from acount.controller import AccountController as AC

import stocks.client as sc

from window.root import RootWindow


class Launcher:
    def __init__(self):
        self.version = "1.0.0"
        self.name = "STALKER"

        print(f"Welcome to {self.name}! Sorry that you have to use the seen console edition, but it can't be helped.")

        self.account_controller = AC()

        self.false_account = False
        self.file_location = None
        self.user = None

        self.stock_client = sc

        self.root = RootWindow(self)

    def set_user_data(self, user):
        self.user = user

    def reset_user_data(self):
        self.false_account = False

        self.user = None

        self.file_location = None

    def save_file(self):
        json_data = self.account_controller.to_jason(self.user)
        file_path = self.file_location
        print(self.user["color"])
        self.account_controller.account_creator.save_data(file_path, json_data, self.user["file"]["encrypted"])

    def start(self):
        self.root.init_root_data()
        self.root.layout()
        self.root.set_binds()

        return self

    def run(self):
        self.root.launch()

        return self


if __name__ == '__main__':
    Launcher().start().run()
