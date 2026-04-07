# Create the Car class
class Car:
      def __init__(self, make, model, year):
          self.make = make
          self.model = model
          self.year = year
      def show(self):
          print(self.make)
          print(self.model)
          print(self.year)

# Create an object
c1 = Car("Ram", "1500", 2020)
# Call the show method
c1.show()