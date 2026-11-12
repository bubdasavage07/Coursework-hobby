"""Read a text file with Python's os library."""

import os


# Put the text file in the same folder as this program.
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "random_words.txt")

if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as word_file:
        words = word_file.read().splitlines()

    print(f"Read {len(words)} words from {os.path.basename(file_path)}:\n")
    for word in words:
        print(word)
else:
    print(f"File not found: {file_path}")
