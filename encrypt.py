#!usr/bin/env python3
import sys
from cryptography.fernet import Fernet
import requests
import hashlib

ip = "192.168.1.1" # REPLACE WITH IP OF THE MACHINE RUNNING SERVER.PY

def encrypt(path):
    key = Fernet.generate_key()
    f = Fernet(key)

    with open(str(path), "rb") as file:
        content = file.read()
    encrypted = f.encrypt(content)
    with open(str(path), "wb") as file:
        file.write(encrypted)

    return encrypted, key

def main(path, password, ip):
    path = path.replace("\\", "/").split("/")[-1]
    content, key = encrypt(path)


    r = requests.post(f"http://{ip}:8000/save", json = {
        "name": str(path),
        "content": str(hashlib.sha256(content).hexdigest()),
        "hash": str(hashlib.sha256(password.encode('UTF-8')).hexdigest()),
        "key": key.decode("ascii")
    })
    if r.status_code == 200:
        print("Successfully encrypted!")
    else:
        print("Something went wrong!")


if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2], ip)
    else:
        print("Usage: encrypt.py <file> <password>")
