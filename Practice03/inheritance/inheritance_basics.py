#1 example

class Animal:
    def speak(self):
        print("Animal makes a sound")

class Dog(Animal):
    pass

d = Dog()
d.speak()

#2 example

class Animal:
    def eat(self):
        print("Eating...")

class Cat(Animal):
    def meow(self):
        print("Meow!")

c = Cat()
c.eat()
c.meow()

#3 example

class Animal:
    def speak(self):
        print("Some sound")

class Bird(Animal):
    def speak(self):
        print("Chirp")

b = Bird()
b.speak()

#4 example

class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, grade):
        super().__init__(name)
        self.grade = grade

s = Student("Alex", 11)
print(s.name, s.grade)
