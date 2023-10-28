import secrets
import string

def shuffle(_list: list):
    if (len(_list) < 2):
        return _list

    resultList = []
    while (len(_list) > 1):
        x = secrets.randbelow(len(_list) - 1)
        resultList.append(_list[x])
        del _list[x]
    resultList.append(_list[0])
    return resultList

def generatePassword(_len: int = 12):
    if (_len < 12): _len = 12

    spec = list(string.punctuation)
    lower = list(string.ascii_lowercase)
    upper = list(string.ascii_uppercase)
    digits = list(string.digits)
    all_chars = spec + lower + upper + digits

    if (_len > len(all_chars) - 1): _len = len(all_chars) - 1

    rawPasswordString = {
        secrets.choice(spec),
        secrets.choice(lower),
        secrets.choice(upper),
        secrets.choice(digits),
    }
    
    while (len(rawPasswordString) < _len):
        rawPasswordString.add(secrets.choice(all_chars))

    return ''.join(shuffle(list(rawPasswordString)))
