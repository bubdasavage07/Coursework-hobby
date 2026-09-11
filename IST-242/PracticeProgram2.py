"""IST 242 practice: working with predefined functions."""


def shout_it_out(text):
    """Convert text to uppercase, print it, and return its length."""
    shouted_text = text.upper()
    print(shouted_text)
    print(f"Length: {len(shouted_text)}")
    return len(shouted_text)


def first_and_last(word):
    """Return the first and last character of a word."""
    if not word:
        raise ValueError("word cannot be empty")
    return word[0], word[-1]


def range_checker(number, minimum, maximum):
    """Return True when number is within the inclusive range."""
    return minimum <= number <= maximum


def count_matches(numbers, target):
    """Count occurrences of target in a list of numbers."""
    return numbers.count(target)


if __name__ == "__main__":
    shout_it_out("python")
    first, last = first_and_last("computer")
    print(f"First: {first}; Last: {last}")
    print(f"15 is in range 10 through 20: {range_checker(15, 10, 20)}")
    print(f"Number of 4s: {count_matches([4, 2, 4, 7, 4, 9], 4)}")
