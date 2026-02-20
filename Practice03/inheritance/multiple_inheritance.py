#1 example

class Animal:
    def speak(self):
        print("Some sound")

class Pet:
    def play(self):
        print("Playing with pet")

class Dog(Animal, Pet):
    def bark(self):
        print("Woof!")

dog = Dog()
dog.speak()  
dog.play()   
dog.bark()   

#2 example

class Vehicle:
    def move(self):
        print("Vehicle moves")

class Flying:
    def move(self):
        print("Flying in the sky")

class FlyingCar(Vehicle, Flying):
    def move(self):
        Vehicle.move(self)
        Flying.move(self)
        print("Flying car is moving")

fc = FlyingCar()
fc.move()

#3 example

class Person:
    def __init__(self, name):
        self.name = name

class Employee:
    def __init__(self, position):
        self.position = position

class Manager(Person, Employee):
    def __init__(self, name, position):
        Person.__init__(self, name)
        Employee.__init__(self, position)

m = Manager("Alice", "Team Lead")
print(m.name)     
print(m.position) 

#4 example

class A:
    def show(self):
        print("A")

class B(A):
    def show(self):
        print("B")

class C(A):
    def show(self):
        print("C")

class D(B, C):
    pass

d = D()
d.show()  
print(D.mro())  
