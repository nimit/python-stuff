import heapq


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

    def file_search(self, prefix: str):
        results = []
        for key, val in self.files.items():
            if prefix in key:
                # results.append((val, key))
                heapq.heappush(results, (val, key))

        # return list(sorted(results, reverse=True)[:10])
        return heapq.nlargest(10, results)


if __name__ == "__main__":
    server = Server(24000)
    server.file_upload("cars.txt", 640)
    server.file_upload("car.txt", 20)
    server.file_upload("carz.txt", 20)
    print(server.file_search("car"))
