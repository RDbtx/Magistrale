import hashlib

m = hashlib.md5()
grade = b"I accept my grade of 18 "
m.update(grade)
to_collide = m.hexdigest()[0:6]
print(to_collide)

#to_collide mi restituisce l'hash del voto
#sfruttando le vulnerabilità di md.5 posso far crescere
#la stringa all infito aggiungendo numeri finche i due
#messaggi diversi avranno lo stesso hash

n = hashlib.md5()
new_grade = b"I accept my grade of 30 "
n.update(new_grade)
collide = n.hexdigest()[0:6]
k = 0

#faccio un append di qualsiasi numero alla stringa
#fino a che gli hash non combaceranno
while collide != to_collide:
  k = k + 1
  temp = "I accept my grade of 30 " + str(k)
  encoded_temp = temp.encode()
  n.update(encoded_temp)
  collide = n.hexdigest()[0:6]

print(collide)

