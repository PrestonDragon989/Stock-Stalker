import json

import base64
from cryptography.fernet import Fernet
import zlib


class Content:
    _fernet_key = "OTVJbnU5YnFkSzMyVko5dHdyaHhCTGVGczk3SThlcktFNTdmN3pFTnhQaz0=".encode()

    def __init__(self, data: str):
        self._raw_data = data
        self._decoded_data = None
        self._encoded_data = None
        self._pure_data = None

    def _get_unencrypted_data(self, raw_data: str or bytes) -> str:
        cipher = Fernet(base64.b64decode(self._fernet_key))
        # zlib => Base64 => Cryptography.Fernet => Normal
        data = zlib.decompress(raw_data.encode() if type(raw_data) is not bytes else raw_data)
        data = base64.b64decode(data)
        return cipher.decrypt(data).decode()

    def _get_encrypted_data(self, raw_data: str) -> bytes:
        cipher = Fernet(base64.b64decode(self._fernet_key))
        # Normal => Cryptography.Fernet => Base64 => zlib
        data = cipher.encrypt(raw_data.encode())
        data = base64.b64encode(data)
        return zlib.compress(data)

    def decrypt_data(self, custom_data=None) -> str:
        data = self._raw_data if custom_data is None else custom_data
        self._decoded_data = self._get_unencrypted_data(data)
        return self._decoded_data

    def encrypt_data(self, decode: bool = False) -> str or bytes:
        self._encoded_data = (self._get_encrypted_data(self._raw_data))
        if decode:
            self._encoded_data = self._encoded_data.decode()
        return self._encoded_data

    def get_pure_data(self, json_str: str or None = None) -> dict:
        self._pure_data = json.loads(self._decoded_data if json_str is None else json_str)
        return self._pure_data

    def save_data(self, data: dict, file: str):
        json_data = json.dumps(data)
        encoded_json_data = self._get_unencrypted_data(json_data)
        with open(file, "a") as file:
            file.write(encoded_json_data)

    @property
    def raw_data(self):
        return self._raw_data

    @raw_data.setter
    def raw_data(self, new_raw_data):
        self._raw_data = new_raw_data

    @property
    def encrypted_data(self):
        return self._encoded_data

    @encrypted_data.setter
    def encrypted_data(self, new_data):
        self._encoded_data = new_data

    @property
    def decrypted_data(self):
        return self._decoded_data

    @decrypted_data.setter
    def decrypted_data(self, new_data):
        self._decoded_data = new_data
