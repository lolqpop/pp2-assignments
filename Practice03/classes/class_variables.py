#1 example

class Car:
    wheels = 4

c1 = Car()
c2 = Car()

c1.wheels = 3

print(c1.wheels)  # 3
print(c2.wheels)  # 4

#2 example

class Car:
    wheels = 4

Car.wheels = 6

c = Car()
print(c.wheels)  # 6

#3 example

class Car:
    def __init__(self, color):
        self.color = color  # instance variable

c1 = Car("red")
c2 = Car("blue")

print(c1.color)  # red
print(c2.color)  # blue

#4 example

class Car:
    wheels = 4  # class variable

c1 = Car()
c2 = Car()

print(c1.wheels)  # 4
print(c2.wheels)  # 4
