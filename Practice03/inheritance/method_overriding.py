#1 example

class Animal:
    def speak(self):
        print("Some generic sound")

class Dog(Animal):
    def speak(self):
        print("Woof!")  

a = Animal()
a.speak()  

d = Dog()
d.speak()

#2 example

class Vehicle:
    def move(self):
        print("Vehicle moves")

class Car(Vehicle):
    def move(self):
        super().move()  
        print("Car drives on road")  

c = Car()
c.move()

#3 example

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

#4 example

class Person:
    def introduce(self):
        print("Hello, I'm a person.")

class Programmer(Person):
    def introduce(self):
        super().introduce()  
        print("And I write Python code.") 

p = Programmer()
p.introduce()

