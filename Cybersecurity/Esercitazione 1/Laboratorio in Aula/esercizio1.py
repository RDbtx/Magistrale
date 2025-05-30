

import math as mt
from Crypto.Util.number import long_to_bytes, bytes_to_long

# il messaggio cifrato è:
message = 11700901449779765763508101081

# sapendo che e = 2 posso calcolare e come:
m = int(mt.sqrt(message))

# traduco in bytes
decrypted = long_to_bytes(m)
print(decrypted)

