#1 example

fruits = ["Apple", "Banana", "Pear", "Orange"]

for f in fruits:
    if f == "Pear":
        print("Pear has found. Stopping the loop.")
        break
    print(f"Checking: {f}")
#2 example

nums = [1, 3, 7, 9, 2]
for n in nums:
    if n == 7:
        break
    print(n)

#3 example

numbers = [4, 6, 2, -1, 8]
for n in numbers:
    if n < 0:
        break
    print(n)

#4 example

names = ["Alice", "Bob", "Charlie", "David", "Eve"]
count = 0

for name in names:
    print(name)
    count = count + 1
    if count == 3:
        break

#5 example

count = 0
while count < 10:
    if count == 3:
        break
    print(count)
    count += 1


