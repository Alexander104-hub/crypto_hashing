from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad
import base64
import binascii

def decrypt_eax(ciphertext, key, tag, nonce):
    key = bytes_from_str(key)
    tag = bytes_from_str(tag)
    nonce = bytes_from_str(nonce)
    ciphertext = base64.b64decode(ciphertext.encode('utf-8') + b'==')
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    decrypted_bytes = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_bytes.decode('utf-8')

def decrypt_cbc(ciphertext, key, iv):
    key = bytes_from_str(key)
    iv = bytes_from_str(iv)
    ciphertext = base64.b64decode(ciphertext.encode('utf-8') + b'==')
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted_bytes = unpad(cipher.decrypt(ciphertext), AES.block_size)
    print(iv)
    return decrypted_bytes.decode('utf-8')


def decrypt_ebc(ciphertext, key):
    key = bytes_from_str(key)
    ciphertext = base64.b64decode(ciphertext.encode('utf-8') + b'==')
    decipher = AES.new(key, AES.MODE_ECB)
    decrypted_bytes = unpad(decipher.decrypt(ciphertext), AES.block_size)
    return decrypted_bytes.decode('utf-8')

# def decrypt(ciphertext, key, tag, nonce, mode):
#     return modes[mode](ciphertext, key, tag, nonce)


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