#1 example

def sum(*args):
    total = 0
    for num in args:
        total += num
    return total

print(sum(1, 2, 3))      
print(sum(5, 10, 15, 2)) 

#2 example

def show(*args):
    for item in args:
        print(item)

show("apple", "banana", "cherry")

#3 example

def user_info(**kwargs):
    for key, value in kwargs.items():
        print(key, ":", value)

user_info(name="Alex", age=18, city="Almaty")

#4 example

def example(*args, **kwargs):
    print("args:", args)
    print("kwargs:", kwargs)

example(1, 2, 3, a=10, b=20)


