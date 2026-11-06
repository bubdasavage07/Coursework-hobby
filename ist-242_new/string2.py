"""
#slicing a phone number
phone = input("Enter phone number as (xxx) yyy-zzzz: ")
areacode = phone[1:4]
prefix = phone[6:9]
suffix = phone[10:]
print ('Area code: ', areacode)
print ('Prefix', prefix)
print ('Suffix', suffix)
"""
"""
#initials from first and last names using find()
name = input("Enter first and last names separated by a space: ")
spacepos = name.find('')
if spacepos == -1:
    print('Error, space not found')
elif name.count(' ')>1:
    print('Error, too many spaces')
else:
    initials = name[0]+name[spacepos+1]
    print(initials)
"""

#Email validation
email = input('Enter email address: ')
if '@' not in email:
    print('missing @')
else:
    dotpos = email.rfind('.')
    if dotpos == -1 or dotpos < email.find('@'):
        print('missing . after @')
    else:
        print('ok')