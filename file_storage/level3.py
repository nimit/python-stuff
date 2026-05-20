import heapq
from datetime import datetime, timedelta


class File:
    size: int
    create_at: datetime
    expire_at: datetime | None

    def __init__(self, create_at, size, ttl=None):
        self.size = size
        self.create_at = datetime.fromisoformat(create_at)
        self.expire_at = (
            None if ttl is None else self.create_at + timedelta(seconds=ttl)
        )

    def exists(self, timestamp: str):
        time = datetime.fromisoformat(timestamp)
        if self.create_at > time:
            return False
        if self.expire_at is None or self.expire_at > time:
            return True
        return False

    def __str__(self):
        return f"{self.size} | Created: {self.create_at.isoformat(timespec='seconds')} | Expired: {self.expire_at.isoformat(timespec='seconds') if self.expire_at is not None else None}"

    def __repr__(self):
        return f"{self.size} | Created: {self.create_at.isoformat(timespec='seconds')} | Expired: {self.expire_at.isoformat(timespec='seconds') if self.expire_at is not None else None}"


class Server:
    files: dict[str, list[File]]
    limit: int

    def __init__(self, limit: int):
        self.limit = limit
        self.files = {}

    def file_upload(self, timestamp, file_name: str, size: int, ttl: int | None = None):
        if size > self.limit:
            raise ValueError("File size exceeds limit")

        file_history = self.files.get(file_name, [])
        for file in file_history:
            if file.exists(timestamp):
                raise ValueError("File already exists")

        self.files.setdefault(file_name, [])
        self.files[file_name].append(File(timestamp, size, ttl))

    def file_get(self, timestamp, file_name: str):
        file_history = self.files.get(file_name, [])
        if len(file_history) > 0 and file_history[-1].exists(timestamp):
            return file_history[-1].size
        return None

    def file_copy(self, timestamp, src: str, dest: str):
        if self.file_get(timestamp, src) is None:
            raise ValueError("File not present")

        now = datetime.fromisoformat(timestamp)
        file_history = self.files[src]
        src_file = file_history[-1]

        # replacement file (if already present) expire at to now
        if self.file_get(timestamp, dest) is not None:
            dest_file = self.files[dest][-1]
            dest_file.expire_at = now
        else:
            self.files.setdefault(dest, [])

        # new replacement should get a modified ttl
        new_ttl = None
        if src_file.expire_at is not None:
            new_ttl = (src_file.expire_at - now).seconds
        self.files[dest].append(File(timestamp, src_file.size, new_ttl))

    def file_search(self, timestamp, prefix: str):
        results = []
        for key, val in self.files.items():
            if prefix in key and val[-1].exists(timestamp):
                # heapq.heappush(results, (val[-1], key))
                results.append((val[-1], key))

        # return heapq.nlargest(10, results, key=lambda x: (x[0].size, x[1]))
        return sorted(results, key=lambda x: (x[0].size, x[1]), reverse=True)[:10]


if __name__ == "__main__":
    server = Server(24000)
    server.file_upload("2021-07-01T12:00:00", "Python.txt", 150)
    server.file_upload("2021-07-01T12:00:00", "CodeSignal.txt", 150, 3600)
    print(server.file_get("2021-07-01T13:00:01", "Python.txt"))
    server.file_copy("2021-07-01T12:00:00", "Python.txt", "PythonCopy.txt")
    print(server.file_search("2021-07-01T12:00:00", "Py"))
    server.file_upload("2021-07-01T12:00:00", "Expired.txt", 100, 1)
    print(server.file_get("2021-07-01T12:00:02", "Expired.txt"))
    server.file_copy("2021-07-01T12:00:00", "CodeSignal.txt", "CodeSignalCopy.txt")
    print(server.file_search("2021-07-01T12:00:00", "Code"))
