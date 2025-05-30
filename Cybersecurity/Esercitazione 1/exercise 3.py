# imported rsa and hashlib function to manipulate rsa and hash encryption
import rsa
import hashlib

# imported pypdf , reportlab and io in order to manipulate PDF files
import pypdf
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io


# function that extract public and private key from .pem files
def loadKeys():
    with open(public_key_path, 'rb') as p:
        publicKey = rsa.PublicKey.load_pkcs1(p.read())
    with open(private_key_path, 'rb') as p:
        privateKey = rsa.PrivateKey.load_pkcs1(p.read())
    return privateKey, publicKey


# it's used to decrypt text from rsa encryption
def decrypt(ciphertext, private_key):
    try:
        return rsa.decrypt(ciphertext, private_key)
    except:
        return False


# it decrypts the encrypted pdf file and creates a new decrypted pdf file
def file_decryption(file_path, private_key_, output_file):
    with open(file_path, 'rb') as enc_file:
        encrypted_data = enc_file.read()

    decrypted_data = decrypt(encrypted_data, private_key_)

    with open(output_file, 'wb') as dec_file:
        dec_file.write(decrypted_data)

# this function is used to modify pdf metadata in order to modify the hash
# of the pdf file
def modify_pdf(pdf_path, original_hash, k_values):
    reader = PdfReader(pdf_path)
    writer = PdfWriter(pdf_path)
    modified_data = "Riccardo Deidda" + str(k_values)
    writer.metadata = {}
    writer.add_metadata({
        "/Author": modified_data,
        "/Producer": "CTRM Course",
    })

    with open(pdf_path, "wb")as file:
        writer.write(file)



# creates the original collision.pdf with the "Riccardo Deidda 70/90/00639"
def write_pdf_collision():
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont('Helvetica', 25)
    can.drawString(100, 500, "Riccardo Deidda 70/90/00639")
    can.save()

    new_pdf = PdfReader(packet)

    output = PdfWriter()

    output.add_page(new_pdf.pages[0])
    output.add_metadata({
        "/Author": "Riccardo Deidda",
        "/Producer": "CTRM Course",
    })

    output_stream = open("collision.pdf", "wb")
    output.write(output_stream)
    output_stream.close()


# its used to calculate pdf file's hash
def hash_calculator(path):
    with open(path, 'rb') as pdf:
        pdf_content = pdf.read()
        pdf_hash = hashlib.sha256(pdf_content).hexdigest()
    return pdf_hash


# Modifies the input PDF file until the first four characters of its hash match the target value.
def collide_pdfs(our_file_path, obj_hash, our_hash):
    k = 0
    print("hash obbiettivo:", obj_hash[0:4])
    while our_hash[0:4] != obj_hash[0:4]:
        k = k + 1
        modify_pdf(our_file_path, our_hash, k)
        our_hash = hash_calculator(our_file_path)
    print("hash modificato", our_hash[0:4])
    print("Collisione creata!")



# Creates the path for each file.
file_path = "C:/Users/ricca/Desktop/CryptoAssignment/exercise3/exercise3.pdf.enc"
private_key_path = "C:/Users/ricca/Desktop/CryptoAssignment/exercise3/keys/privateKey.pem"
public_key_path = "C:/Users/ricca/Desktop/CryptoAssignment/exercise3/keys/publicKey.pem"
decrypted_pdf = "file_decrypted.pdf"
collision_pdf = "collision.pdf"

# This section of the code extracts the private and
# public keys from .pem files and decrypts the exercise3.pdf.enc file.
private_key_, public_key = loadKeys()
file_decryption(file_path, private_key_, decrypted_pdf)

# calculates the objective hash witch is the hash from the exercise3.pdf file
obj_hash = hash_calculator(decrypted_pdf)

# a collision.pdf file with the string "Riccardo Deidda 70/90/00639" is created
# and it's hash gets calculated from the hash_calculator function
write_pdf_collision()
our_hash = hash_calculator(collision_pdf)

# The collide_pdf function is called, which modifies collide.pdf until
# its hash matches the hash of the decrypted file.
collide_pdfs(collision_pdf, obj_hash, our_hash)

