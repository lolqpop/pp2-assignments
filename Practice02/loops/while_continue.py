#1 example

i = 0
while i < 5:
    i = i + 1
    if i == 3:
        continue  
    print(i)

#2 example

number = 0
while number < 6:
    number = number + 1
    if number % 2 != 0:  
        continue
    print(f"{number} is an even number")

#3 example

books = ["New Book", "Damaged Book", "Old Book"]
while books:
    current = books.pop(0)
    if "Damaged" in current:
        print("Skipping a damaged book")
        continue
    print(f"Adding {current} to the shelf.")

#4 example

while True:
    name = input("Enter a name (at least 3 letters): ")
    if name == "exit":
        break
    if len(name) < 3:
        print("Too short! Try again.")
        continue  
    print(f"Hello, {name}!")

#5 example

total = 0
count = 0
while count < 3:
    val = int(input("Enter a positive number: "))
    if val < 0:
        print("You have to enter a positive number. We will skip this.")
        continue
    total = total + val
    count = count + 1

print(f"The total sum is: {total}")