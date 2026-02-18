#1 example

def greetings(name): # name is a parameter
    print(f"Hello, {name}!")
greetings("Pasha") # 'Pasha' is an argument

#2 example

def standart(nam = "Ayan"):
    print(f"My name is {nam}")
standart("Nursultan")
standart("Daniar")
standart()

#3 example

def vegetables(veg):
    for i in veg:
        print(i)
bag = ["tomato", "cucumber", "broccolli"]
vegetables(bag)

#4 example

def func(bird, people):
    print(f"I have {bird}")
    print(f"This is my friend {people}")
func(people = "Tobias", bird = "bucky")