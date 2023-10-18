import hashlib
from pathlib import Path
import os
import json


class Hash:
    def __init__(self):
        self.__hashes = {}
    def compute_file_hash(self, filepath: str):
        path = Path(filepath)
        hashes = {}
        if not path.exists():
            raise FileNotFoundError("File or folder doesn't exist")

        hashes[filepath] = self.__dir_to_list(filepath)
        self.__hashes = hashes
        with open("./hashes.json", "w") as file:
            json.dump(self.__hashes, file, indent=4)


    def __dir_to_list(self, dirname, path=os.path.pathsep):
        data = {}
        for file_name in os.listdir(dirname):
            fullpath = os.path.join(dirname, file_name)
            if os.path.isdir(fullpath):
                data[file_name] = self.__dir_to_list(fullpath) 
            elif os.path.isfile(fullpath):
                data[file_name] = self.__get_hash(fullpath)
        return data

    def __get_hash(self, file: str):
        with open(file, "rb") as out_file:
            digest = hashlib.file_digest(out_file, "sha256")
        return digest.hexdigest() 