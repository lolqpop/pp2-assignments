n = int(input("Input your number: "))
def numbers(a):
    cnt  = 1
    while cnt <= a:
        if cnt % 3 == 0 and cnt % 4 == 0:
            yield cnt
        cnt  += 1

for num in numbers(n):
    print(num)