import json
import os
import time
from base64 import b64decode
from datetime import datetime, timezone
from importlib.resources import open_text
from types import SimpleNamespace

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA


class SnapTradeUtils:
    @classmethod
    def convert_to_simple_namespace(cls, data):
        """Converts json data into python object"""
        if type(data) == list:
            data = {"class_name": "SimpleNamepace", "data": data}
        else:
            data["class_name"] = "SimpleNamepace"
        serialized_data = json.dumps(data)

        return json.loads(serialized_data, object_hook=lambda d: SimpleNamespace(**d))

    @classmethod
    def get_api_endpoints(cls):
        with open_text("snaptrade.api_client", "endpoints.json") as f:
            return json.load(f)

    @classmethod
    def get_epoch_time(cls):
        return int(time.time())

    @classmethod
    def get_utc_time(cls, string_format=None):
        if string_format:
            return datetime.now(timezone.utc).strftime(string_format)
        else:
            return datetime.now(timezone.utc)

    @classmethod
    def generate_rsa_key(cls):
        """Generates a private and public rsa key"""
        key = RSA.generate(2048, os.urandom)

        private_key = key.exportKey("PEM").decode()

        public_key = key.publickey().exportKey("OpenSSH")

        return private_key, public_key

    @classmethod
    def decrypt_rsa_message(cls, encrypted_message, private_key):
        """
        Decrypt an RSA encrypted message

        Private_key should be a string
        """

        private_key = RSA.import_key(private_key)

        cipher = PKCS1_OAEP.new(private_key)

        return cipher.decrypt(b64decode(encrypted_message.encode())).decode()

    @classmethod
    def decrypt_aes_message(cls, shared_key, encrypted_message, tag, nonce):
        """
        Decrypt an aes message that was encrypted using AES.MODE_OCB

        shared_key is expected to be a string

        This method assumes that the encrypted_message, tag and nonce were b64 encoded strings.
        """

        b64_decoded_nonce = b64decode(nonce)
        b64_decoded_message = b64decode(encrypted_message)
        b64_decoded_tag = b64decode(tag)

        cipher = AES.new(shared_key.encode(), AES.MODE_OCB, nonce=b64_decoded_nonce)

        return cipher.decrypt_and_verify(b64_decoded_message, b64_decoded_tag).decode()
