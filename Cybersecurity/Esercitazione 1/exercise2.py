# I've imported pypdf to manipulate pdf data and Cryptodome
# for the AES decrypt and unpad funciton
import pypdf
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad

# Since I noticed through several attempts that decoding an incorrectly
# deciphered text results in an error, I created a function that discards
# all the errors and returns only the correct message and the simmetric key
def message_checker(encrypted_message):

    # i created a for loop that iterates through every combination of zeroes and ones
    # in a string composed by 16 characters in order to bruteforce the encription key
    length = 16
    for i in range(2 ** length):
        key = format(i, f'0{length}b')
        key = key.encode()

        # then i used the AES decrypt function to decrypt the message with each possible key
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted_text = cipher.decrypt(encrypted_message)

        # Since, while searching for a solution to this exercise,
        # I noticed that trying to decode a wrongfully decrypted message returned an error,
        # I created this "try: except:" condition to return only the decryption
        # instance that didn’t produce any errors.
        try:
            possible_message = decrypted_text.decode()
        except:
            pass

        # If no errors are returned, then the function has found the key and the deciphered message
        else:
            # i used to remove eventual padding from the message. I had to cast .encode() in order to
            # use the unpad function
            clearmessage = unpad(possible_message.encode(),16)
            return clearmessage.decode(), key.decode()


# points to the pdf file inside the computer
file_path = "C:/Users/ricca/Desktop/CryptoAssignment/exercise2/exercise2.pdf"
pdf = pypdf.PdfReader(file_path)

# Gets the encrypted message from the PDF and converts it from hex to bytes.
encrypted_message_hex = pdf.pages[0].extract_text()
encrypted_message = bytes.fromhex(encrypted_message_hex)

#returns the plaintext and the encryption key
print(message_checker(encrypted_message))





