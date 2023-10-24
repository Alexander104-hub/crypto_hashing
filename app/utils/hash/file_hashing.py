import hashlib
from pathlib import Path
import os
import json


class Hash:
    def __init__(self):
        self.__hashes = {}
    def compute_file_hash(self, filepath: str, hash_algo):
        path = Path(filepath)
        hashes = {}
        if not path.exists():
            raise FileNotFoundError("File or folder doesn't exist")


        if path.is_dir():
            hashes[filepath] = self.__dir_to_list(filepath, hash_algo)
        elif path.is_file():
            hashes[filepath] = self.__get_hash(filepath, hash_algo)


        self.__hashes = hashes
        with open("./hashes.json", "w") as file:
            json.dump(self.__hashes, file, indent=4)

        return self.__hashes 


    def __dir_to_list(self, dirname, hash_algo):
        data = {}
        for file_name in os.listdir(dirname):
            fullpath = os.path.join(dirname, file_name)
            if os.path.isdir(fullpath):
                data[file_name] = self.__dir_to_list(fullpath, hash_algo) 
            elif os.path.isfile(fullpath):
                data[file_name] = self.__get_hash(fullpath, hash_algo)
        return data

    def __get_hash(self, file: str, hash_algo):
        with open(file, "rb") as out_file:
            digest = hashlib.file_digest(out_file, hash_algo)
        return digest.hexdigest() 
