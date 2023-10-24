from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import binascii


def decrypt(ciphertext, key, tag, nonce):
    key = bytes_from_str(key)
    tag = bytes_from_str(tag)
    nonce = bytes_from_str(nonce)
    ciphertext = base64.b64decode(ciphertext.encode('utf-8') + b'==')
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    decrypted_bytes = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_bytes.decode('utf-8')

def decrypt_file(ciphertext, key, tag, nonce):
    key = bytes_from_str(key)
    tag = bytes_from_str(tag)
    nonce = bytes_from_str(nonce)
    ciphertext = base64.b64decode(ciphertext + b'==')
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    decrypted_bytes = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_bytes

def bytes_from_str(raw_str: str):
    # return raw_str.replace('\\\\', '\\').encode().decode('unicode_escape').encode('latin1')
    return binascii.unhexlify(raw_str)