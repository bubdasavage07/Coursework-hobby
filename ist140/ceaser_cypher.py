import string
import random

#Purpose: Create a cipher using the caesar algorithm with a shift
# 1. randomly generate an 8 letter password
# 2. encrypt the password
# 3. the encrypted password includes a 2 digit value at the front which equals the shift
# 4. store 5 encrypted passwords into an array

#the complete lowercase alphabet in string form
alpha =string.ascii_lowercase
print(alpha)
#is alpha in list/character form
beta =list(alpha)
print(beta)
#the value of the shift
shift = 5

position =alpha.index("e")
print(position)

#alpha at position shift-1
"""
gamma #helper variable
delta #encrypted alphabet
password
encPass
"""
def id_generator(size=6, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

#print(string.ascii_lowercase)
#print(string.ascii_uppercase)
#print(string.digits)
#print(string.punctuation)
#print(string.printable)

#print(id_generator())

password = id_generator()

password2 = list(password)

print(password)
print(password2)



