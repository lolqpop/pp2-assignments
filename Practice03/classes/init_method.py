#1 example

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p1 = Person("Alex", 18)
print(p1.name)
print(p1.age)

#2 example

class Person:
    def __init__(self, name):
        self.name = name

    def hello(self):
        return f"Hi, my name is {self.name}"

p = Person("Alex")
print(p.hello())

#3 example

class Counter:
    def __init__(self):
        self.value = 0

    def increase(self):
        self.value += 1

c = Counter()
c.increase()
c.increase()
print(c.value)  

#4 example

class Cat:
    def __init__(self, name):
        self.name = name  

    def say(self):
        print(f"{self.name} : meow")


my_cat = Cat("Barsik")
my_cat.say()