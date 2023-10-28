from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import base64
import binascii


def encrypt_eax(text, random_key, **kwargs):
    if kwargs['nonce']:
        cipher = AES.new(random_key, AES.MODE_EAX, nonce=bytes.fromhex(kwargs['nonce']))
    else:
        cipher = AES.new(random_key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(text)
    ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    random_key = bytes_to_str(binascii.hexlify(random_key))
    tag = bytes_to_str(binascii.hexlify(tag))
    nonce = bytes_to_str(binascii.hexlify(cipher.nonce))
    return {'Шифротекст: ': ciphertext, 'Ключ: ': random_key, 'Тег: ': tag, 'Одноразовый код: ': nonce}


def encrypt_cbc(text, random_key, **kwargs):
    if kwargs['iv']:
        cipher = AES.new(random_key, AES.MODE_CBC, iv=bytes.fromhex(kwargs['iv']))
    else:
        cipher = AES.new(random_key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(text, AES.block_size))
    ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    iv = bytes_to_str(binascii.hexlify(cipher.iv))
    random_key = bytes_to_str(binascii.hexlify(random_key))
    return {'Шифротекст: ': ciphertext, 'Ключ: ': random_key, 'IV: ': iv}

def encrypt_ebc(text, random_key, **kwargs):
    cipher = AES.new(random_key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(text, AES.block_size))
    ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    random_key = bytes_to_str(binascii.hexlify(random_key))
    return {'Шифротекст: ': ciphertext, 'Ключ: ': random_key}

modes = {
    'EAX': encrypt_eax,
    'CBC': encrypt_cbc,
    'ECB': encrypt_ebc
}


def encrypt(text, mode, key, nonce=None, iv=None):
    text = text.encode('utf-8')
    if key:
        random_key = bytes.fromhex(key)
    else:
        random_key = get_random_bytes(16)
    return modes[mode](text, random_key, nonce=nonce, iv=iv)

# TODO: add CBC and ECB algs for files
def encrypt_file(file):
    random_key = get_random_bytes(16)
    cipher = AES.new(random_key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(file)
    return base64.b64encode(ciphertext), bytes_to_str(binascii.hexlify(random_key)), bytes_to_str(binascii.hexlify(tag)), bytes_to_str(binascii.hexlify(cipher.nonce))

def bytes_to_str(b: bytes):
    return str(b)[2:-1]
