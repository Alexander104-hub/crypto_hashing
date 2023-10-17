from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import ast

def decrypt(ciphertext: str, key: str, tag: str, nonce: str):
    key = bytes_from_str(key)
    tag = bytes_from_str(tag)
    nonce = bytes_from_str(nonce)
    ciphertext = base64.b64decode(ciphertext.encode('utf-8'))
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    return str(cipher.decrypt_and_verify(ciphertext, tag)).replace('b\'', '').replace('\'', '')


def bytes_from_str(string: str):
    string = f'b\'{string}\''.replace('\\\\', '\\')
    return ast.literal_eval(string)