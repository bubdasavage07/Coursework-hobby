# Week 12
# Searching, Sorting and Files review

"""
Sorting a list of values
"""
numbertext = "12 8 4 0 16 9 13 17 1 18 14 6 2 3 7 11 15 10 19 5"
numberlist = (numbertext.split())
print(numberlist)

numbertext2 = "17, 8, 4, 11, 16, 9, 13, 12, 1, 18, 14, 7, 2, 3, 6, 0, 15, 10, 19, 5"
numberlist2 = (numbertext2.split())

#numberlist2 = numbertext2.replace(",", "").split() #Option 1
numberlist2 = [item.strip(",") for item in numbertext2.split()] #Option 2
#numberlist2 = [int(x) for x in numbertext2.replace(",", "").split()]
print(numberlist2)

# Sort the original number list
numberlist.sort()
print(numberlist)

numberlist.sort(key=int) #sort by integer value, but as a string
print(numberlist)

numberlist = [int(x) for x in numbertext.split()] #convert string values to integer
numberlist.sort()
print(numberlist)

"""
Searching a string
"""
text = "python programming is like pizza..."
print(f"Text: '{text}'")

# User input: a letter
letter = input("Enter a letter to search for: ")

# Count how many times the letter appears
count = text.count(letter)

# Check if it's there and display the result
if count > 0:
    print(f"Yes! The letter '{letter}' appears {count} time(s).")
else:
    print(f"The letter '{letter}' is not in the text.")


"""
Reading files
"""
sample_words = "apple banana cherry dragon elephant forest guitar honey iguana jungle kite lemon mountain nebula ocean planet quartz river telescope umbrella"
with open("words.txt", "w") as f:
    f.write(sample_words)

#Open and read the file
with open("words.txt", "r") as file:
    content = file.read()

# Split the content into a list of individual words
word_list = content.split()

#cDisplay the results
print(f"Total words found: {len(word_list)}")
print("Word list:", word_list)

with open("words.txt", "r") as file:
    # This creates a list where each line is a separate item
    word_list2 = [line.strip() for line in file]
    print(word_list2)




