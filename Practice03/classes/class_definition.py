#1 example

class Dog:
    def bark(self):
        return "woof"

d = Dog()
print(d.bark())

#2 example

class Car:
    wheels = 4

c1 = Car()
c2 = Car()

print(c1.wheels)
print(c2.wheels)

#3 example

class Person:
    pass

p = Person()
p.name = "Alex"
p.age = 18

print(p.name, p.age)

#4 example

class Person: # simplest way to create a class
    pass

