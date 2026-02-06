#1 example

nums = [1, 2, 3, 4, 5]

for n in nums:
    if n == 3:
        continue  
    print(f"Number: {n}")

#2 example

d = [1, 2, 3, 4, 5, 6, 7, 8]

for num in d:
    if num % 2 != 0:  
        continue
    print(f"Even: {num}")

#3 example

names = ["Alice", "", "Bob", "   ", "Charlie"]

for name in names:
    if name.strip() == "": 
        continue
    print(f"Valid name: {name}")

#4 example

for i in range(1, 10):
    if i % 3 == 0:
        continue
    print(i)

#5 example

messages = ["Hello!", "(Spam)", "Meeting at 5", "(Spam)"]

for msg in messages:
    if "Spam" in msg:
        continue
    print(f"New message: {msg}")