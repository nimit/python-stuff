class Server:
    files: dict
    limit: int

    def __init__(self, limit: int):
        self.limit = limit
        self.files = {}

    def file_upload(self, file_name: str, size: int):
        if size > self.limit:
            raise ValueError("File size exceeds limit")

        if file_name in self.files:
            raise ValueError("File already exists")

        self.files[file_name] = size

    def file_get(self, file_name: str):
        return self.files.get(file_name, None)

    def file_copy(self, src: str, dest: str):
        if src not in self.files:
            raise ValueError("File not present")

        size = self.files.pop(src)
        self.files[dest] = size
