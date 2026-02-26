n = int(input("Input your number: "))
def declin(a):
    while a>=0:
        yield a 
        a -= 1

for num in declin(n):
    print(num)