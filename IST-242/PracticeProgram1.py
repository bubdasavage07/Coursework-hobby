"""IST 242 practice: syntax and basic math operations."""

import math


def rectangle_area(length, width):
    """Return the area of a rectangle."""
    return length * width


def triangle_area(base, height):
    """Return the area of a triangle."""
    return (base * height) / 2


def circle_area(radius):
    """Return the area of a circle."""
    return math.pi * radius**2


def split_the_bill(total_amount, number_of_people):
    """Return each person's equal share of a bill."""
    if number_of_people <= 0:
        raise ValueError("number_of_people must be greater than zero")
    return total_amount / number_of_people


def calculate_tip(bill_amount):
    """Return tip amounts at 18%, 20%, and 25%."""
    return {
        "18%": bill_amount * 0.18,
        "20%": bill_amount * 0.20,
        "25%": bill_amount * 0.25,
    }


def even_or_odd(number):
    """Return whether an integer is even or odd."""
    return "even" if number % 2 == 0 else "odd"


if __name__ == "__main__":
    length = float(input("Enter the rectangle length: "))
    width = float(input("Enter the rectangle width: "))
    print(f"Rectangle area: {rectangle_area(length, width)}")

    base = float(input("Enter the triangle base: "))
    height = float(input("Enter the triangle height: "))
    print(f"Triangle area: {triangle_area(base, height)}")

    radius = float(input("Enter the circle radius: "))
    print(f"Circle area: {circle_area(radius):.2f}")

    total_amount = float(input("Enter the total bill amount: $"))
    number_of_people = int(input("Enter the number of people: "))
    print(f"Each person pays: ${split_the_bill(total_amount, number_of_people):.2f}")

    bill_amount = float(input("Enter a bill amount to calculate the tip: $"))
    for percentage, amount in calculate_tip(bill_amount).items():
        print(f"Tip at {percentage}: ${amount:.2f}")

    number = int(input("Enter an integer to check if it is even or odd: "))
    print(f"{number} is {even_or_odd(number)}")
