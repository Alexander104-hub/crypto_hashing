from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import binascii

def encrypt(text):
    text = text.encode('utf-8')
    random_key = get_random_bytes(16)
    cipher = AES.new(random_key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(text)
    return base64.b64encode(ciphertext).decode('utf-8'), bytes_to_str(binascii.hexlify(random_key)), bytes_to_str(binascii.hexlify(tag)), bytes_to_str(binascii.hexlify(cipher.nonce))

def bytes_to_str(b: bytes):
    return str(b)[2:-1]