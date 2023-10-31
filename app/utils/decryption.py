from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import binascii

def to_b64(text, file=False):
    if not file:
        text = text.encode('utf-8') + b'=='
    return base64.b64decode(text)


def decrypt_eax(ciphertext, key, tag, nonce, file=False):
    key = bytes_from_str(key)
    tag = bytes_from_str(tag, hexlify = False)
    nonce = bytes_from_str(nonce, hexlify = False)
    ciphertext = to_b64(ciphertext, file)
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    decrypted_bytes = cipher.decrypt_and_verify(ciphertext, tag)
    if not file:
        return decrypted_bytes.decode('utf-8')
    return decrypted_bytes

def decrypt_cbc(ciphertext, key, iv, file=False):
    key = bytes_from_str(key)
    iv = bytes_from_str(iv)
    ciphertext = to_b64(ciphertext, file)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted_bytes = unpad(cipher.decrypt(ciphertext), AES.block_size)
    if not file:
        return decrypted_bytes.decode('utf-8')
    return decrypted_bytes


def decrypt_ebc(ciphertext, key, file=False):
    key = bytes_from_str(key)
    ciphertext = to_b64(ciphertext, file)
    decipher = AES.new(key, AES.MODE_ECB)
    decrypted_bytes = unpad(decipher.decrypt(ciphertext), AES.block_size)
    if not file:
        return decrypted_bytes.decode('utf-8')
    return decrypted_bytes


def decrypt_file(ciphertext, mode, key, iv, tag, nonce):
    if mode == 'CBC':
        decrypted_bytes = decrypt_cbc(ciphertext, key, iv, True)
    elif mode == 'ECB':
        decrypted_bytes = decrypt_ebc(ciphertext, key, True)
    else:
        decrypted_bytes = decrypt_eax(ciphertext, key, tag, nonce, True)
    return decrypted_bytes

def bytes_from_str(raw_str: str, hexlify = True):
    # use hexlify = False if youre not usign passgenerator.generatePassword...
    # ...function.
    # return raw_str.replace('\\\\', '\\').encode().decode('unicode_escape').encode('latin1')
    if hexlify:
        raw_str = raw_str.encode("utf-8").hex()
    return binascii.unhexlify(raw_str)
