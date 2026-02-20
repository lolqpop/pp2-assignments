#1 example

class Animal:
    def speak(self):
        print("Some generic sound")

class Dog(Animal):
    def speak(self):
        super().speak() 
        print("Woof!")

d = Dog()
d.speak()

#2 example

class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, grade):
        super().__init__(name)
        self.grade = grade

s = Student("Alice", 10)
print(s.name)   
print(s.grade) 

#3 example

class A:
    def show(self):
        print("A")

class B(A):
    def show(self):
        print("B")
        super().show()

class C(A):
    def show(self):
        print("C")
        super().show()

class D(B, C):
    def show(self):
        print("D")
        super().show()  

d = D()
d.show()
print(D.mro())

#4 example

class Vehicle:
    def move(self):
        print("Vehicle moves")

class Car(Vehicle):
    def move(self):
        super().move()  
        print("Car drives on road") 

c = Car()
c.move()
