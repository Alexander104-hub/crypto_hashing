from jsondiff import diff


class HashDiff:
    def __init__(self):
        self.template = ""
    def preprocess_file_with_hashes(self, file_content):
        if type(eval(file_content)) != dict:
            raise TypeError('Content is not json')
        return eval(file_content)

    def compute_diff(self, hash1, hash2):
        return self.__handle_diff_result(diff(hash1, hash2,\
                                              syntax='explicit', marshal=True))

    def __handle_diff_result(self, result):
        self.diff_template(result)
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
                self.template += f"{element}: {json[element]}<br>"
        self.template += "</details>"
