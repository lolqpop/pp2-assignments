#1 example

sum = lambda a, b: a + b
print(sum(3, 7))  

#2 example

is_even = lambda x: x % 2 == 0
print(is_even(4))  
print(is_even(5))  

#3 example

def func(n):
    return lambda a: a*n
funn = func(3)
print(funn("ahahah"))

#4 example

def f(v):
    return lambda c: c+v
vc = f(4)
print(vc(5))