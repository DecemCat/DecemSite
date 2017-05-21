from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class AESUtil():
    @staticmethod
    def encrypt(key, text, iv):
        key_len = len(key)
        if key_len > 24:
            key = key[0:23]
        elif key_len < 24:
            key = key + ''.join([' ' for i in range(24 - key_len)])


        iv_len = len(iv)
        if iv_len > 16:
            iv = iv[0:15]
        elif iv_len < 16:
            iv = iv + ''.join([' ' for i in range(16 - iv_len)])

        cryptor = AES.new(key, AES.MODE_CBC, iv)
        length = 16
        count = len(text)
        if count < length:
            add = (length-count)
            text = text + ('\0' * add)
        elif count > length:
            add = (length-(count % length))
            text = text + ('\0' * add)
        ciphertext = cryptor.encrypt(text)
        return b2a_hex(ciphertext)

    @staticmethod
    def decrypt(key, text, iv):
        key_len = len(key)
        if key_len > 24:
            key = key[0:23]
        elif len(key) < 24:
            key = key + ''.join([' ' for i in range(24 - key_len)])

        iv_len = len(iv)
        if iv_len > 16:
            iv = iv[0:15]
        elif iv_len < 16:
            iv = iv + ''.join([' ' for i in range(16 - iv_len)])
        cryptor = AES.new(key, AES.MODE_CBC, iv)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')
