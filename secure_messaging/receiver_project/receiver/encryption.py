from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class MessageEncryption:
    def __init__(self, key=None):
        if key is None:
            key = self.generate_key()
        self.fernet = Fernet(key)

    @staticmethod
    def generate_key():
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'secure_salt',
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(b'shared_secret'))
        return key

    def encrypt_message(self, message):
        return self.fernet.encrypt(message.encode())

    def decrypt_message(self, encrypted_message):
        return self.fernet.decrypt(encrypted_message).decode()