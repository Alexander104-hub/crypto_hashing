import hashlib


class Hash:
    def __init__(self):
        self.__hashes = {}
        self.__CHUNK_SIZE = 1024 ** 2 # Default: 1024 (bytes) ** 2 = 1MB;
    async def compute_file_hash(self, *files, hash_algo):
        for file in files[0]:
            self.__hashes[file.filename] = self.__get_hash(file, hash_algo)
        return self.__structured_json(self.__hashes)


    def __structured_json(self, hashes: dict):
        result = {}
        keys = sorted(hashes.keys(), key=lambda x: len(x.split('/')))
        for key in keys:
            exec_string = "result"
            splited_key = key.split('/')
            for part in splited_key:
                if len(part.split('.')) >= 2 and \
                    not part.startswith('.') or splited_key[-1] == part:
                    exec_string += f"['{part}'] = '{hashes[key]}'"
                else:
                    exec_string += f"['{part}']"
                    try:
                        exec(exec_string)
                    except KeyError:
                        exec(exec_string + " = {}")
            exec(exec_string)
        return result

    def __get_hash(self, file, hash_algo):
        hash_func = hashlib.new(hash_algo)
        while content := file.file.read(self.__CHUNK_SIZE):
            hash_func.update(content)
        return hash_func.hexdigest() 
