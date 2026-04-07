import string
import random

#Purpose: Create a cipher using the caesar algorithm with a shift
# 1. randomly generate an 8 letter password
# 2. encrypt the password
# 3. the encrypted password includes a 2 digit value at the front which equals the shift
# 4. *** store 5 encrypted passwords into an array - not complete

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
pseudo code:
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

#alternate and direct way of assigning the beta variable as a list
beta = list(string.ascii_lowercase)
print("beta = ", beta)

#randomize the shift
shift = random.randrange(1, 100)
print("Random shift value = ", shift)
shift = shift % len(beta)
print("Test shift is less than 26: ", shift)

#create a string of the encrypted alphabet based on the shift
delta = beta[shift:] + beta[:shift]
print("".join(delta))

#alternate way to break apart the original alphabet string
gamma = []
shift = 5
for index, letter in enumerate(beta):       
    if index >= shift:
        gamma.append(letter)
for index, letter in enumerate(beta):       
    if index < shift:
        gamma.append(letter)
print()
print("Encrypted alphabet is: ")
print(gamma)


"""
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


