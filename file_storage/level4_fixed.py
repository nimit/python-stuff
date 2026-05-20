import heapq
from datetime import datetime, timedelta


class File:
    size: int
    create_at: datetime
    expire_at: datetime | None
    overwritten_expiration: datetime | None

    def __init__(self, create_at, size, ttl=None):
        self.size = size
        self.create_at = datetime.fromisoformat(create_at)
        self.expire_at = (
            None if ttl is None else self.create_at + timedelta(seconds=ttl)
        )
        self.overwritten_expiration = None

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

    def __lt__(self, other):
        return self.size < other.size

    def __gt__(self, other):
        return self.size > other.size

    def __eq__(self, other):
        return self.size == other.size


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

    def _get_latest_alive_file(self, timestamp: str, file_name: str) -> File | None:
        history = self.files.get(file_name, [])
        for file in reversed(history):
            if file.exists(timestamp):
                return file
        return None

    def file_get(self, timestamp, file_name: str):
        file = self._get_latest_alive_file(timestamp, file_name)
        return None if file is None else file.size

    def file_copy(self, timestamp, src: str, dest: str):
        if self.file_get(timestamp, src) is None:
            raise ValueError("File not present")

        now = datetime.fromisoformat(timestamp)
        file_history = self.files[src]
        src_file = file_history[-1]

        # replacement file (if already present) expire at to now
        dest_file = self._get_latest_alive_file(timestamp, dest)
        if dest_file is not None:
            dest_file.overwritten_expiration = dest_file.expire_at
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
            if key.startswith(prefix):
                file = self._get_latest_alive_file(timestamp, key)
                if file is not None:
                    heapq.heappush(results, (val[-1], key))
                # results.append((val[-1], key))

        return heapq.nlargest(10, results, key=lambda x: (x[0].size, x[1]))
        # return sorted(results, key=lambda x: (x[0].size, x[1]), reverse=True)[:10]

    def rollback(self, timestamp):
        time = datetime.fromisoformat(timestamp)
        for key, history in self.files.items():
            for file_variant in history[::-1]:
                if file_variant.create_at > time:
                    history.pop()
                else:
                    if file_variant.overwritten_expiration is not None:
                        # When the file was overwritten by a copy but we are rolling back to a time before the overwrite (this is the latest file variant in the history at the given `timestamp`)
                        file_variant.expire_at = file_variant.overwritten_expiration
                        file_variant.overwritten_expiration = None
                    break


if __name__ == "__main__":
    server = Server(24000)
    server.file_upload("2021-07-01T12:00:00", "Initial.txt", 100)
    server.file_upload("2021-07-01T12:05:00", "Update1.txt", 150, 3600)
    print(server.file_get("2021-07-01T12:10:00", "Initial.txt"))
    server.file_copy("2021-07-01T12:15:00", "Update1.txt", "Update1Copy.txt")
    server.file_upload("2021-07-01T12:20:00", "Update2.txt", 200, 1800)
    server.rollback("2021-07-01T12:10:00")
    print(server.file_get("2021-07-01T12:25:00", "Update1.txt"))
    print(server.file_get("2021-07-01T12:25:00", "Initial.txt"))
    print(server.file_search("2021-07-01T12:25:00", "Up"))
    print(server.file_get("2021-07-01T12:25:00", "Update2.txt"))
