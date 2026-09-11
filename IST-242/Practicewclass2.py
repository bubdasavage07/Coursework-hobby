

word = "hamburger"
num = 10

def ShoutWord():
    print(word.upper())
    print(len(word))

def CheckRange():
    if num in range(1,10):
        print("yes")
    else:
        print("no")
    
def firstLast():
    print(word[0],word[-1])

def countNum():
    count = 0
    letter = "r"
    for i in word:
        if i==letter:
            count+=1
    print(count)



ShoutWord()
CheckRange()
firstLast()
countNum()
