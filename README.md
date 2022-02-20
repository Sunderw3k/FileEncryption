# File Encryption

This is a simple python script which uses cryptogrphy.Fernet to encrypt the contents of a file.   

## Usage

```
pip install -r requirements.txt
python server.py # on the machine you want to host the database
# Change the IP in encrypt.py and decrypt.py to the IP of the hosting machine
python encrypt.py <file> <pass>
python decrypt.py <file> <pass>
```

## How it works  

When using encrypt.py the script sends a POST request to the machine running server.py.
That machine stores the filename, Fernet hashed contents, hashed password and the hashed Fernet key.
When decrypting the script sends the file contents and the password to see if we can find the entry in the database, if yes we send back the key.
