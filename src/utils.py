import hashlib


def hash_sha256(string: str) -> str:
    hasher = hashlib.sha256()
    hasher.update(string.encode("utf-8"))
    return hasher.hexdigest()
