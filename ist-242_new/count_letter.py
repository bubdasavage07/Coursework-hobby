"""Count how many times a user-chosen letter appears in a string."""

text = input("Enter a string: ")
letter = input("Enter one letter to search for: ")

if len(letter) != 1:
    print("Please enter exactly one letter.")
else:
    count = text.lower().count(letter.lower())
    print(f"The letter '{letter}' appears {count} time(s).")
