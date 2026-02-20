#1 example

class Student:
    def __init__(self, name):
        self.name = name

    def info(self):
        print("Student name:", self.name)

s = Student("Alex")
s.info()

#2 example

class Counter:
    def __init__(self):
        self.value = 0

    def increase(self):
        self.value += 1
c = Counter()
c.increase()
c.increase()
print(c.value)  # 2

#3 example

class User:
    def __init__(self, age):
        self.age = age

    def can_vote(self):
        if self.age >= 18:
            return True
        return False
u = User(16)
print(u.can_vote())  # False

#4 example

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height
r = Rectangle(4, 5)
print(r.area())  # 20
