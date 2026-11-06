# Simple text processor with assignment and concatenation
"""
text = '' # initialize as empty string
entry = input('> ') # input() returns a string
while entry != '': # string compare
    command = entry[0] # character access
    if   command == '=': text = input('>> ')   # assignment
    elif command == '+': text += input('>> ')  # concatenation
    elif command == '-': text = ''             # reset to empty string
    print(text)
    entry = input('> ')
"""

# Simple text processor with slicing
"""
text = ''
entry = input('> ')
while entry != '':
    command = entry[0]
    if   command == '+': text += entry[1:] # slice and concatenate
    elif command == '-': text = ''
    else:                text = entry
    print(text)
    entry = input('> ')
""" 

"""
# Simple text processor to demonstrate some string features
text = ''
entry = input('> ')
while entry != '':
    display = False
    command = entry[0]
    if command == '+':
        text += entry[1:] # slice and concatenate
        display = True
    elif command == '-':
        text = '' # reset to empty string
    elif command == '?':
        print(entry[1:] in text) # search
    elif command == '#':
        print(text.count(entry[1:])) # count
    else:
        text = entry

    if display:
       print(text)
    entry = input('> ')
"""