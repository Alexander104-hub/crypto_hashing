import json
from jsondiff import diff
from pathlib import Path
from ...exceptions import file_exceptions


class HashDiff:
    def preprocess_file_with_hashes(self, path):
        __path = Path(path)
        if not __path.exists():
            raise FileNotFoundError('IncorrectPath. File doesnt found.')

        if __path.is_dir():
            # Return error, incorrect path.
            raise file_exceptions.IncorrectPath("Path is a dir.")

        if __path.is_file():
            file_ext = __path.name.split('.')[-1]
            print(file_ext)
            if file_ext != 'json':
                raise file_exceptions.IncorrectFileExt("Incorrect file extenteion. Require: .json")
            # Open it and return file's content.
            with open(__path, "r") as file:
                file_content = file.read()
            if x := type(eval(file_content)) != dict: # check for strs and dicts
                print(x)
                raise TypeError('Content is not json')
            return eval(file_content)

    def compute_diff(self, hash1, hash2):
        return self.__handle_diff_result(diff(hash1, hash2,\
                                              syntax='explicit', marshal=True))

    def __handle_diff_result(self, result):
        #hash1 is 'older' than hash2
        return json.dumps(result, indent=4)

"""
hash1 must be done earlier than hash2

Overview:
root folder:
    updated:
        summary:
            folder_1:
                main.py: hash_1 -> hash_2
            folder_2:
                index.html: hash_1 -> hash_2
    summary:
        deleted:
            __init__.py


<summary>
"""

