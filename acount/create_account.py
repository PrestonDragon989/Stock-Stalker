import json
import os.path

from acount.content import Content

from window.utils.color import color_palette
from datetime import datetime


class AccountCreator:
    _today = datetime.today().strftime('%m-%d-%y')

    _base_colors_dict = color_palette.copy()
    _base_user_dict = {
        "name": "",
        "preferred_name": "",
        "password": "",
        "date_created": _today,
        "last_login": _today,
    }
    _base_file_dict = {
        "encrypted": False
    }
    _base_stocks_dict = {
        "followed": [],
        "placeholder_stocks": {}
    }

    @staticmethod
    def save_data(file_path: str, json_data: str, encrypted: bool):
        content = Content(json_data)
        if encrypted:
            data = content.encrypt_data()
            if not os.path.exists(file_path):
                with open(file_path, "wb") as file:
                    file.write(data)
            else:
                open(file_path, "w")
                with open(file_path, "wb") as file:
                    file.write(data)

            content.encrypted_data = data
        else:
            data = content.raw_data
            with open(file_path, "w") as file:
                file.write(data)

    def create_base_account(self, name: str, pref_name: str, password: str, encrypted: bool, js: bool = False) \
            -> dict or str:
        print(self._base_colors_dict)
        data = {"file": self._base_file_dict, "user": self._base_user_dict,
                "color": self._base_colors_dict, "stocks": self._base_stocks_dict}
        data["user"]["name"] = name
        data["user"]["preferred_name"] = pref_name
        data["user"]["password"] = password

        data["file"]["encrypted"] = encrypted

        return self.full_create_account(data, is_json=js)

    @staticmethod
    def full_create_account(data, is_json=False) -> dict or str:
        account = {
            "file": {
                "encrypted": data["file"]["encrypted"]
            },
            "user": {
                "name": data["user"]["name"],
                "preferred_name": data["user"]["preferred_name"],
                "password": data["user"]["password"],
                "date_created": data["user"]["date_created"],
                "last_login": data["user"]["last_login"],
            },
            "color": {
                "main_bg": data["color"]["main_bg"],
                "second_bg": data["color"]["second_bg"],
                "third_bg": data["color"]["third_bg"],
                "foreground": data["color"]["foreground"],
                "active_ground": data["color"]["active_ground"],
                "grid_color": data["color"]["grid_color"],
                "stock_color": data["color"]["stock_color"],
                "border_color": data["color"]["border_color"]
            },
            "stocks": {
                "followed": data["stocks"]["followed"],
                "placeholder_stocks": data["stocks"]["placeholder_stocks"],
            }
        }

        if is_json:
            return json.dumps(account)
        return account

    def is_valid(self, save_object: dict) -> bool:
        compare_object = self.create_base_account(" ", " ", " ", True)
        for key in ["file", "user", "stocks", "color"]:
            if key not in save_object:
                return False

        return True

    @property
    def today(self):
        return self._today

    @today.setter
    def today(self, new_today):
        self._today = new_today
