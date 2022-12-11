# A simple notes app
# Made by @sociallyencrypted

import os
from flag import FLAG


def hexify(text):
    s = ""
    for c in text:
        r = hex(ord(c))[2:]
        if len(r) == 1:
            r = "0" + r
        s += r
    return s


def nexify(hexx):
    return "".join([chr(int(hexx[i : i + 2], 16)) for i in range(0, len(hexx), 2)])


def encrypt(plaintext, key):
    block = key
    ciphertext = ""
    for i in range(len(plaintext) // len(key)):
        for j in range(len(key)):
            ciphertext += chr(ord(plaintext[i * len(key) + j]) ^ ord(block[j]))
        block = ciphertext[-len(key) :]
    return hexify(ciphertext)


def decrypt(ciphertext, key):
    block = key
    plaintext = ""
    for i in range(len(ciphertext) // len(key)):
        for j in range(len(key)):
            plaintext += chr(ord(ciphertext[i * len(key) + j]) ^ ord(block[j]))
        block = ciphertext[i * len(key) : (i + 1) * len(key)]
    return plaintext


MENU = """
WELCOME TO SOCIALLYENCRYPTED'S NOTE APP (WITH ASCII SUPPORT!)
1. Add note
2. View note
3. Exit
-------------------------------------------------------------"""

count = 0


def addNote(text):
    files = [f for f in os.listdir(".") if os.path.isfile(f) and ".txt" in str(f)]
    filecounts = [int(file[:-4]) for file in files]
    filecounts.sort(reverse=True)
    if len(files) > 0:
        count = filecounts[0] + 1
    else:
        count = 1
    # ---ENCRYPT---
    key = input("Enter key to encrypt the note: ")
    if len(text) % len(key) != 0:
        padding = "=" * (len(key) - (len(text) % len(key)))
        print(padding)
    else:
        padding = ""
    text = encrypt(text + padding, key)
    # ---ENCRYPT---
    with open(str(count) + ".txt", "w") as f:
        f.write(text)
    print("Note added: ", count)


def readNote(count):
    key = input("Enter key to decrypt the note: ")
    with open(str(count) + ".txt", "r") as f:
        ciphertext = f.read()
    print("Ciphertext: ", ciphertext)
    ciphertext = nexify(ciphertext)
    # print(len(ciphertext), len(key))
    if len(ciphertext) % len(key) == 0:
        plaintext = decrypt(ciphertext, key)
        while plaintext[-1] == "=":
            plaintext = plaintext[:-1]
        if count == 1:
            if plaintext == FLAG:
                print(FLAG)
            else:
                print("You got to the flag, but the key is not right!")
                print("First few charachters decrypted using given key:", plaintext[: len(key)])
        else:
            print("Decrypted plaintext:", plaintext)
    else:
        print("Invalid key length.")
        return


while True:
    print(MENU)
    choice = input("Enter your choice: ")
    if choice == "1":
        text = input("Enter note: ")
        addNote(text)
    elif choice == "2":
        count = int(input("Enter note number: "))
        readNote(count)
    elif choice == "3":
        exit()
