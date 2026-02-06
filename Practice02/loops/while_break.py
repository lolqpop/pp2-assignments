#1 example 

while True:
    word = input("Say something (or 'stop'): ")
    if word == "stop":
        break  
    print("You said", word)

#2 example

while True:
    password = input("Enter password: ")
    if password == "secret123":
        print("Access granted!")
        break
    print("Wrong password. Try again.")

#3 example

number = 1
while number <= 10:
    if number == 7:
        print("Found the lucky number 7!")
        break
    print("Checking:", number)
    number = number + 1

#4 example

total_price = 0
while True:
    price = int(input("Enter item price: "))
    total_price = total_price + price
    if total_price > 50:
        print("You spent too much! Stopping.")
        break
    print("Total so far:", total_price)

#5 example

lives = 3
while lives > 0:
    action = input("Did you win the round? (yes/no): ")
    if action == "yes":
        print("You won the game!")
        break
    lives = lives - 1
    print(f"You lost a life. Lives left: {lives}")