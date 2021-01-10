from base64 import b64decode
import hashlib
from Cryptodome.Cipher import AES
import os
from Cryptodome.Random import get_random_bytes
import getpass
import json

def decrypt(enc_dict, password):
    # decode the dictionary entries from base64
    salt = b64decode(enc_dict['salt'])
    cipher_text = b64decode(enc_dict['cipher_text'])
    nonce = b64decode(enc_dict['nonce'])
    tag = b64decode(enc_dict['tag'])
    

    # generate the private key from the password and salt
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    # create the cipher config
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

    # decrypt the cipher text
    try:
        decrypted = cipher.decrypt_and_verify(cipher_text, tag)
    except:
        decrypted = "ERROR: worong password"

    return decrypted

if not os.path.isfile('archive.crypto'):
    print("No encripted file found")
else:
    file = open("archive.crypto", "r")
    data = json.load(file)
    print("Avaiable data:")
    for tag in data:
        print(f"\t{tag}")
    tag = input("Data to decrypt: ")
    if tag in data:
        pswd = getpass.getpass('Password: ')
        print(decrypt(data[tag], pswd).decode())
    else:
        print("Name not found")