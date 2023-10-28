import base64
import binascii

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from ..utils.passgenerator import passgenerator


def encrypt_eax(text, random_key):
    cipher = AES.new(random_key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(text)
    ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    tag = binascii.hexlify(tag).decode()
    nonce = binascii.hexlify(cipher.nonce).decode()
    random_key = random_key.decode()
    return {'Шифротекст: ': ciphertext, 'Ключ: ': random_key, 'Тег: ': tag, 'Одноразовый код: ': nonce}


def encrypt_cbc(text, random_key, iv = passgenerator.generatePassword(16)):
    cipher = AES.new(random_key, AES.MODE_CBC, iv = iv.encode())
    ciphertext = cipher.encrypt(pad(text, AES.block_size))
    ciphertext = base64.b64encode(ciphertext).decode()
    iv = cipher.iv.decode()
    random_key = random_key.decode()
    return {'Шифротекст: ': ciphertext, 'Ключ: ': random_key, 'IV: ': iv}

def encrypt_ecb(text, random_key):
    cipher = AES.new(random_key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(text, AES.block_size))
    ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    random_key = random_key.decode()
    return {'Шифротекст: ': ciphertext, 'Ключ: ': random_key}

modes = {
    'EAX': encrypt_eax,
    'CBC': encrypt_cbc,
    'ECB': encrypt_ecb,
}


def encrypt(text, mode, key, key_len = 16):
    # key_len must be divisible by 8, max value is 32
    if not key:
        key = passgenerator.generatePassword(key_len)
    text = text.encode('utf-8')
    random_key = bytes(key, "UTF-8")
    return modes[mode](text, random_key)

# TODO: add CBC and ECB algs for files
def encrypt_file(file):
    random_key = get_random_bytes(16)
    cipher = AES.new(random_key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(file)
    return base64.b64encode(ciphertext), bytes_to_str(binascii.hexlify(random_key)), bytes_to_str(binascii.hexlify(tag)), bytes_to_str(binascii.hexlify(cipher.nonce))

def bytes_to_str(b: bytes):
    return str(b)[2:-1]
