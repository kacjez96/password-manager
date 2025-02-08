import json
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto import Random

# Model
class Model:
    def __init__(self, filepath_db="passwords_db.json", filepath_log="master_secret.json"):
        self.__filepath_db = filepath_db
        self.__filepath_log = filepath_log
        self.master_secret = self.load_master_secret()
        self.passwords = self.load_passwords()

        block_size = 16
        self.padding = lambda s: s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size)
        self.unpadding = lambda s: s[:-ord(s[len(s) - 1:])]
        self.key = None

    def set_key(self, key):
        self.key = key

    def load_master_secret(self):
        with open(self.__filepath_log, "r") as file:
            temp_pass = json.load(file)
            print(temp_pass)
            return temp_pass['master_secret']

    @staticmethod
    def hash(passwd):
        passwd_b = passwd.encode('utf-8')
        hash = hashlib.sha256(passwd_b, usedforsecurity=True)
        passwd_hash = hash.hexdigest()
        return passwd_hash

    def load_passwords(self):
        try:
            with open(self.__filepath_db, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_passwords(self):
        with open(self.__filepath_db, "w") as file:
            json.dump(self.passwords, file, indent=4)

    def add_password(self, title, login, password):
        password = self.encrypt(password)
        self.passwords.append({"title": title, "login": login, "password": password, "visible": False})
        for x in self.passwords:
            if x['visible']:
                x['password'] = self.encrypt(x['password'])
                x['visible'] = False
        self.save_passwords()

    def get_passwords(self):
        return self.passwords

    def delete_password(self, index):
        if 0 <= index < len(self.passwords):
            del self.passwords[index]
            self.save_passwords()

    def encrypt(self, password):
        private_key = hashlib.sha256(self.key.encode("utf-8")).digest()
        password = str.encode(self.padding(password))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        temp = base64.b64encode(iv + cipher.encrypt(password))
        return bytes.decode(temp)

    def show_password(self, index):
        private_key = hashlib.sha256(self.key.encode("utf-8")).digest()
        password = self.passwords[index]['password'].encode("utf-8")
        password = base64.b64decode(password)
        iv = password[:16]
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        temp = self.unpadding(cipher.decrypt(password[16:]))
        self.passwords[index]['password'] = bytes.decode(temp)
        self.passwords[index]['visible'] = True
        self.save_passwords()

    def hide_password(self, index):
        password = self.passwords[index]['password']
        self.passwords[index]['password'] = self.encrypt(password)
        self.passwords[index]['visible'] = False
        self.save_passwords()

    def show_hide_password(self, index):
        if not self.passwords[index]['visible']:
            self.show_password(index)
        else:
            self.hide_password(index)

    def __str__(self):
        return f"{self.master_secret}"

    def __len__(self):
        return len(self.passwords)

    def __add__(self, other):
        return Model(self.passwords + other.passwords)

    def __del__(self):
        for i in range(len(self.passwords)):
            if self.passwords[i]['visible']:
                self.hide_password(i)
