# AES 256 encryption/decryption using pycryptodome library

from base64 import b64encode
import hashlib
from Cryptodome.Cipher import AES
import os
from Cryptodome.Random import get_random_bytes
import getpass
import json

def encrypt(plain_text, password):
    # generate a random salt
    salt = get_random_bytes(AES.block_size)

    # use the Scrypt KDF to get a private key from the password
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    # create cipher config
    cipher_config = AES.new(private_key, AES.MODE_GCM)

    # return a dictionary with the encrypted text
    cipher_text, tag = cipher_config.encrypt_and_digest(bytes(plain_text, 'utf-8'))
    return {
        'cipher_text': b64encode(cipher_text).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8')
    }

print("AES encryptor")
text = input("Testo da cryptare: ")
while True:
    pswd = getpass.getpass('Password: ')
    if pswd == getpass.getpass('Re-type your password: '):
        break
    else:
        print("Password don't match")

encryptedText = encrypt(text, pswd)

if not os.path.isfile('archive.crypto'):
    file = open("archive.crypto", "w+")
    file.write("{}")
    file.close()

while True:
    tag = input("Name: ")

    file = open("archive.crypto", "r")
    data = json.load(file)
    if tag in data:
        print("This name alredy exist.")
        response = input("Do you want to overwrite it [Y/N]: ")
        if response == 'y' or response == 'Y':
            break
    else:
        break


with open('archive.crypto', 'r+') as f:
    data = json.load(f)
    data[tag] = encryptedText
    f.seek(0)
    json.dump(data, f, indent=4)
    f.truncate()
