import math


def rectangle_area():
    length = float(input("Enter the rectangle length: "))
    width = float(input("Enter the rectangle width: "))
    area = length * width
    print (area)


def triangle_area():
    base = float(input("Enter the triangle base: "))
    height = float(input("Enter the triangle height: "))
    area= (base * height) / 2
    print (area)


def circle_area():
    radius = float(input("Enter the circle radius: "))
    area= math.pi * radius**2
    print (area)

"""
def split_the_bill():
    total_amount = float(input("Enter the total bill amount: $"))
    number_of_people = int(input("Enter the number of people: "))
    if number_of_people <= 0:
        raise ValueError("number_of_people must be greater than zero")
    return total_amount / number_of_people


def calculate_tip():
    bill_amount = float(input("Enter a bill amount to calculate the tip: $"))
    return {
        "18%": bill_amount * 0.18,
        "20%": bill_amount * 0.20,
        "25%": bill_amount * 0.25,
    }


def even_or_odd():
    number = int(input("Enter an integer to check if it is even or odd: "))
    return f"{number} is {'even' if number % 2 == 0 else 'odd'}"


if __name__ == "__main__":
    print(f"Rectangle area: {rectangle_area()}")

    print(f"Triangle area: {triangle_area()}")

    print(f"Circle area: {circle_area():.2f}")

    print(f"Each person pays: ${split_the_bill():.2f}")

    for percentage, amount in calculate_tip().items():
        print(f"Tip at {percentage}: ${amount:.2f}")

    print(even_or_odd())
"""