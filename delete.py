import os
import json

if not os.path.isfile('archive.crypto'):
    print("No encripted file found")
else:
    file = open("archive.crypto", "r")
    data = json.load(file)
    print("Delete data:")
    for tag in data:
        print(f"\t{tag}")
    tag = input("Data to erase [* for all data]: ")
    if tag == '*':
        data = {}
        print("Deleted all data!")
    elif tag in data:
        del data[tag]
        print(f"Deleted {tag}")
    else:
        print("Name not found")
        
    with open('archive.crypto', 'r+') as f:
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()