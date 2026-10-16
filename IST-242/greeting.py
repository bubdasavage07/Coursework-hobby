class Greeting:

    def __init__(self, first, last):
        self.first = first
        self.last = last


    def display (self, formal=False):
        if formal:
            print(f"Hello {self.first} {self.last}")
        else:
            print(f"Hi {self.first}")

    def __str__(self):
        return f"{self.first},{self.last}"

    def __repr__(self):
        return self.__str__()


greeting = Greeting(input("First name: "), input("Last name: "))

greeting.display()
greeting.display(formal=True)
print(greeting)