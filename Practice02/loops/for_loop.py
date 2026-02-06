#1 example

numbers = [10, 20, 30, 40]
t = 0

for num in numbers:
    t = t + num

print("Total sum: " + str(t))

#2 example

i = [1, 5, 2, 5, 3, 5, 4]
cnt = 0

for x in i:
    if x == 5:
        cnt = cnt + 1

print(f"The number 5 appears {cnt} times")

#3 example

d = [1, 2, 3, 4, 5, 6]
evens = []

for n in d:
    if n % 2 == 0:
        evens.append(n)

print(f"Even numbers: {evens}")

#4 example

n = [1, 2, 3, 4, 5]
sq = []

for n in n:
    sq.append(n * n)
print(f"Squares: {sq}")

#5 example

words = ["apple", "banana", "kiwi", "cherry"]
shortest = words[0] 

for w in words:
    if len(w) < len(shortest):
        shortest = w

print(f"The shortest word is: {shortest}")