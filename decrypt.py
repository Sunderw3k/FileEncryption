from cryptography.fernet import Fernet
import sys
import requests
import hashlib

ip = "192.168.1.1" # REPLACE WITH IP OF THE MACHINE RUNNING SERVER.PY

def main(path, password, ip):
    path = path.replace("\\", "/").split("/")[-1]

    with open(path, "rb") as file:
        content = file.read()

    r = requests.post(f"http://{ip}:8000/check", json = {
        "name": str(path),
        "content": str(hashlib.sha256(content).hexdigest()),
        "hash": str(hashlib.sha256(password.encode("UTF-8")).hexdigest())
    })

    if r.text == "404":
        print("Not found!")
        return
    if r.text == "403":
        print("Password Incorrect!")
        return    
    key = r.text[1:-1]
    f = Fernet(key.encode())
    content = f.decrypt(content)

    with open(path, "wb") as file:
        file.write(content)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2], ip)
    else:
        print("Usage: decrypt.py <file> <password>")

