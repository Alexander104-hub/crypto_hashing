import hashlib
from pathlib import Path
import os
import json


class Hash:
    def __init__(self):
        self.__hashes = {}
    async def compute_file_hash(self, *files, hash_algo):
        # if path.is_dir():
        #     hashes[filepath] = self.__dir_to_list(filepath, hash_algo)
        for file in files[0]:
            self.__hashes[file.filename] = self.__get_hash(await file.read(), hash_algo)


        with open("./hashes.json", "w") as file:
            json.dump(self.__hashes, file, indent=4)

        return self.__structured_json(self.__hashes)


    def __structured_json(self, hashes: dict):
        result = {}
        keys = sorted(hashes.keys(), key=lambda x: len(x.split('/')))
        for key in keys:
            exec_string = "result"
            for part in key.split('/'):
                if len(part.split('.')) >= 2:
                    exec_string += f"['{part}'] = '{hashes[key]}'"
                else:
                    exec_string += f"['{part}']"
                    try:
                        exec(exec_string)
                    except KeyError:
                        exec(exec_string + " = {}")
            exec(exec_string)
        return result
            # print(result)
# frontend/index.html
# frontend/static/css/style.css


    def __get_hash(self, content, hash_algo):
        hash_func = hashlib.new(hash_algo)
        hash_func.update(content)
        return hash_func.hexdigest() 
