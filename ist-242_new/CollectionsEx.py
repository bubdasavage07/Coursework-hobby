# Collections examples

#List
#An ordered, mutable (changeable) collection that can hold mixed data types.
#Defined with square brackets [].
my_list = ["apple", 3, True]
print(my_list, "\n")
my_list[0] = "banana" #change item in the first postion of the list
print(my_list, "\n")

#Array
#A typed sequence for numerical data.
#Python requires importing a module like array or numpy for true arrays,
#  because lists are normally used for general collections.
import array as arr

#my_array = arr.array('data type', a list or tuple)
my_array = arr.array('i', [1, 2, 3])  # 'i' means signed integer
print(my_array, "\n")
print(my_array.typecode)  # Outputs: i
print(list(my_array))     # Outputs: [1, 2, 3]

# Pass a list of individual character strings
text_array = arr.array('u', ['h', 'e', 'l', 'l', 'o']) #causes error
print(text_array) #see line above

my_string = "hello"
text_array = arr.array('u', list(my_string))
print(text_array)

print("\n")

#Tuple
# An ordered, immutable (unchangeable) collection. Defined with parentheses ().
my_tuple = (10, 20, 30)
# my_tuple[0] = 5  # Error: tuples cannot be changed
print(my_tuple, "\n")

#Dictionary
#A collection of unique key-value pairs. Defined with curly brackets {}
my_dict = {"name": "Alice", "age": 25}
print(my_dict["name"])  # Accesses "Alice"

# A dictionary storing names as keys and ages as values
my_dict = {
    "Alice": 25,
    "Bob": 30,
    "Charlie": 22
}

# Accessing a specific value using its key
print(my_dict["Bob"])  # Outputs: 30


