import json
import os

from tkinter import filedialog
from tkinter.messagebox import showerror

from acount.content import Content

from acount.create_account import AccountCreator


class AccountController:
    def __init__(self):
        self._account_creator = AccountCreator()

    @staticmethod
    def get_file(file_path) -> str or int:
        """
        This gets the path to the account file, or an error.
        Returns:
            If the file has been successfully gotten, it will return the path. If it doesn't successfully get it,
            it will return an error code (int).

            1 - File not selected (It was None)
            2 - File selected was not a .json file and isn't valid (File other than .json)
        """
        if file_path is None:
            account_file = filedialog.askopenfilename(defaultextension=".json",
                                                      title="Please Select your STALKER save file",
                                                      initialdir=os.curdir + "/saves")
        else:
            account_file = file_path

        if not account_file:
            return 1
        elif os.path.splitext(account_file)[1] != ".json":
            return 2
        else:
            return account_file

    def get_data(self, file_path):
        content = Content("N/A")
        failed = False
        try:
            with open(file_path, "r") as file:
                data = file.read()
                content.decrypted_data = data

        except UnicodeDecodeError:
            with open(file_path, "rb") as file:
                data = file.read()
                try:
                    content.encrypted_data = data
                    content.decrypted_data = content.decrypt_data(data)
                except Exception as e:
                    showerror("Failed to Decrypt", f"Failed to decrypt the given save file. Error: {e}")
                    failed = True
        user_object = {}
        try:
            user_object = content.get_pure_data(content.decrypted_data)
        except Exception as e:
            showerror("Failed to convert", f"Failed to convert the save file to valid data. Error {e}")
            failed = True

        if self._account_creator.is_valid(user_object) is False:
            showerror("Incorrect Json Object", f"The file given is missing pieces, or is not a save file.")

        if failed:
            return None
        return user_object

    @property
    def account_creator(self):
        return self._account_creator

    @staticmethod
    def to_jason(data: dict) -> str:
        return json.dumps(data)


if __name__ == '__main__':
    controller = AccountController()

