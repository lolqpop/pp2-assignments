a = int(input("Input your number: "))
b = int(input("Input your number: "))
def squares(n, m):
    for i in range(n,m+1):
        yield i**2
    
div = squares(a,b)
for i in range(b):
    print(next(div))