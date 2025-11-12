from string import printable
from Cryptodome.Cipher import AES
from Crypto.Util.Padding import pad

def encrypt(plain):
    key = b'0123456789abcedf'
    cipher = AES.new( key, AES.MODE_ECB )
    padded_pt = pad(plain+b'AES-ECB-leaking!', 16)
    return cipher.encrypt(padded_pt).hex()


#algoritmo bruteforce che prende in ingresso il messaggio di 15 bytes + byte sec
def search_algorithm( first_16_bytes_message):

  for i in printable:
    #cifro la possibile soluzione
    bruteforce = "aaaaaaaaaaaaaaa" + str(i)
    bruteforce_b = bruteforce.encode()
    bruteforce_encry = encrypt(bruteforce_b)

    #prendo i primi 16 bit del messaggio cifrato
    first_16_bytes_hex = bruteforce_encry[:32]
    #controllo che corrispondano a quelli in ingresso
    if(first_16_bytes_hex == first_16_bytes_message):

      #se i valori corrispondono ritorno il byte segreto
      return i


#prendo il messaggio base da 15 bit e lo cripto, gli verrà aggiunto il segreto
messaggio = "aaaaaaaaaaaaaaa"
mex_enc = messaggio.encode()
mex_crypt = encrypt(mex_enc)

#sapendo che AES cripta a gruppi di 16, prendo i primi 16 bytes == 32 hex
first_16_bytes_message = mex_crypt[:32]
print(search_algorithm(first_16_bytes_message))