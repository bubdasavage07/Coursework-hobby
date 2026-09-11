import math


amt = float(input("Enter bill amount: $"))

def rec_area():
    length = float(input("Enter length of the rectangle: "))
    width = float(input("Enter width of the rectangle: "))
    area = length * width
    print (area)

def tri_area():
    base = float(input("Enter base of triangle: "))
    height = float(input("Enter height of triangle: "))
    area = (base * height)/2
    print (area)

def cir_area():
    radius = float(input("Enter radius of the circle: "))
    area = math.pi * radius**2
    print (area)


def split_bill():
    global amt
    numPeople =int(input("How many people in the party: "))
    divAmount = amt/numPeople
    print(f"${divAmount:.2f}")

def calc_tip():
    global amt
    tip18 = amt*0.18
    print(f"18%=${tip18:.2f}")
    tip20 = amt*0.2
    print(f"20%=${tip20:.2f}")
    tip25 = amt*0.25
    print(f"25%=${tip25:.2f}")

def EvenOdd():
    global amt
    if amt % 2==0:
        print(amt, "is even")
    else:
        print(amt, "is odd")


rec_area()
tri_area()
cir_area()
split_bill()
calc_tip()
EvenOdd()