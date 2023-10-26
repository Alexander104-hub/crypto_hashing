from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import base64
import binascii


def encrypt_eax(text, random_key):
    cipher = AES.new(random_key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(text)
    ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    random_key = bytes_to_str(binascii.hexlify(random_key))
    tag = bytes_to_str(binascii.hexlify(tag))
    nonce = bytes_to_str(binascii.hexlify(cipher.nonce))
    return {'Шифротекст: ': ciphertext, 'Ключ: ': random_key, 'Тег: ': tag, 'Одноразовый код: ': nonce}


def encrypt_cbc(text, random_key):
    cipher = AES.new(random_key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(text, AES.block_size))
    ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    print(cipher.iv)
    iv = bytes_to_str(binascii.hexlify(cipher.iv))
    random_key = bytes_to_str(binascii.hexlify(random_key))
    print(f'\n\nCIPHER IV: {cipher.iv}\n\n')
    return {'Шифротекст: ': ciphertext, 'Ключ: ': random_key, 'IV: ': iv}



modes = {
    'EAX': encrypt_eax,
    'CBC': encrypt_cbc
}

# def encrypt(text):
#     text = text.encode('utf-8')
#     random_key = get_random_bytes(16)
#     cipher = AES.new(random_key, AES.MODE_EAX)
#     ciphertext, tag = cipher.encrypt_and_digest(text)
#     return base64.b64encode(ciphertext).decode('utf-8'), bytes_to_str(binascii.hexlify(random_key)), bytes_to_str(binascii.hexlify(tag)), bytes_to_str(binascii.hexlify(cipher.nonce))

def encrypt(text, mode):
    text = text.encode('utf-8')
    random_key = get_random_bytes(16)
    return modes[mode](text, random_key)
    cipher = AES.new(random_key, mode)
    ciphertext, tag = cipher.encrypt_and_digest(text)
    return base64.b64encode(ciphertext).decode('utf-8'), bytes_to_str(binascii.hexlify(random_key)), bytes_to_str(binascii.hexlify(tag)), bytes_to_str(binascii.hexlify(cipher.nonce))



def encrypt_file(file):
    random_key = get_random_bytes(16)
    cipher = AES.new(random_key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(file)
    return base64.b64encode(ciphertext), bytes_to_str(binascii.hexlify(random_key)), bytes_to_str(binascii.hexlify(tag)), bytes_to_str(binascii.hexlify(cipher.nonce))

def bytes_to_str(b: bytes):
    return str(b)[2:-1]
