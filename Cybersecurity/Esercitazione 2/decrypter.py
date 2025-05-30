# script used to decrypt the secret message find on pastebin

import base64

def file_opener(filepath):
    with open('message.txt', 'r',) as file:
        messaggi = file.readlines()
        return messaggi


def decode_string(encoded_string):
    try:
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_string = decoded_bytes.decode()
        return decoded_string
    except:
        pass
    try:
        decoded_bytes = base64.b32decode(encoded_string)
        decoded_string = decoded_bytes.decode()
        return decoded_string
    except:
        pass  


    strings = file_opener("message.txt")
    for i in strings:
        print(decode_string(i.strip()))
