import json
from jsondiff import diff
from pathlib import Path
from ...exceptions import file_exceptions


class HashDiff:
    def __init__(self):
        self.template = ""
    def preprocess_file_with_hashes(self, path):
        __path = Path(path)
        if not __path.exists():
            raise FileNotFoundError('IncorrectPath. File doesnt found.')

        if __path.is_dir():
            # Return error, incorrect path.
            raise file_exceptions.IncorrectPath("Path is a dir.")

        if __path.is_file():
            file_ext = __path.name.split('.')[-1]
            if file_ext != 'json':
                raise file_exceptions.IncorrectFileExt("Incorrect file extention. Require: .json")
            # Open it and return file's content.
            with open(__path, "r") as file:
                file_content = file.read()
            if type(eval(file_content)) != dict: # check for strs and dicts
                raise TypeError('Content is not json')
            return eval(file_content)

    def compute_diff(self, hash1, hash2):
        return self.__handle_diff_result(diff(hash1, hash2,\
                                              syntax='explicit', marshal=True))

    def __handle_diff_result(self, result):
        self.diff_template(result)
        # print(self.template)
        # return json.dumps(result, indent=4)
        return self.template

    def diff_template(self, json):
        nl: str = "\n"
        for element in json:
            if isinstance(json[element], dict):
                self.template += f"<details><summary>{element}</summary>"
                self.diff_template(json[element])
            else:
                if isinstance(json[element], list):
                    self.template += f"<details><summary>{element}</summary>{nl.join(json[element])}</details>"
                    continue
                self.template += f"{element}: {json[element]}"
        self.template += "</details>"
