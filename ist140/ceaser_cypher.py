import string
import random

#Purpose: Create a cipher using the caesar algorithm with a shift
# 1. randomly generate an 8 letter password
# 2. encrypt the password
# 3. the encrypted password includes a 2 digit value at the front which equals the shift
# 4. store 5 encrypted passwords into an array

#the complete lowercase alphabet in string form
alpha = string.ascii_lowercase
print(alpha)

#is alpha in list/character form
beta = list(alpha)
print(beta)

#the value of the shift
shift = 5 - 1

position = alpha.index("e")
position2 = alpha[shift-1]
print(position)
print(position2)

#encrypted alphabet
"""
delta = []
delta = find the shift and start there
the value in the shift position is
position 0 of delta
add the remaining letters from beta until Z
(or the end of the list)
go back to 0 or the start of beta and
add remaining letters UNTIL (and including)
the letter D ( < SHIFT-1 )
"""
beta = list(string.ascii_lowercase)
print("beta = ", beta)
shift = 5
shift = shift % len(beta)
delta = beta[shift:] + beta[:shift]
print("".join(delta))



"""
gamma = []
delta = []
for index, letter in enumerate(beta):       
    if index >= shift:
        delta.append(letter)
print(delta)

for index, letter in enumerate(beta):       
    if index < shift:
        gamma.append(letter)
print(gamma)

delta = delta + gamma
print(delta)

#alpha at position shift-1
"""
"""
gamma #helper variable
password
encPass


def id_generator(size=8, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

#print(string.ascii_lowercase)
#print(string.ascii_uppercase)
#print(string.digits)
#print(string.punctuation)
#print(string.printable)

#print(id_generator())

password = id_generator()
print(password)


password2 = list(password)


print(password2)
"""


