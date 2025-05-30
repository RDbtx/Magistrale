# imported pypdf in order to read the pdf
# and cryptodome to use AES decrypt functions
import pypdf
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad


file_path = "C:/Users/ricca/Desktop/CryptoAssignment/exercise1/exercise1.pdf"
pdf = pypdf.PdfReader(file_path)

# i check if there is any useful information inside the pdf
print(pdf)
print(pdf.metadata)
print(pdf.pages[0].extract_text())

# there is the symmetric key in the metadata, i extract it and the crypted message
# simmetric key format is changed to bytes since decrypt function requires bytes input
simmetric_key = pdf.metadata['/SuperSecretECBKey'].encode()
encrypted_message_hex = pdf.pages[0].extract_text()

# convert the encrypted message from hex to bytes
encrypted_message = bytes.fromhex(encrypted_message_hex)

# i use the cryptodome library to decrypt the encrypted message
cipher = AES.new(simmetric_key, AES.MODE_ECB)
decrypted_data = cipher.decrypt(encrypted_message)

# ECB encryption has probably padding inside it so i call the unpad
# function and then specify the block size for the unpadding, i also
# use decode to change the format from bytes to str
clearmessage = unpad(decrypted_data, 16).decode("utf-8")

# the secret message is then printed
print(clearmessage)
