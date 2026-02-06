#1 example

number = 3
while number > 0:
    print(number)
    number = number - 1  
print("GO!")

#2 example

money = 0
while money < 50:
    money = money + 10
    print(f"There are already {money} tenge in the piggy bank")

#3 example

again = "yes"
while again == "yes":
    print("Hello!")
    again = input("Again? (yes/no): ")

#4 example

var = ["ball", "Python", "Bread"]
while var:
    var1 = var.pop()  
    print(f"Here is {var1}")

print("Empty!")

#5 example

x = 2
while x <= 10:
    print(x)
    x = x + 2  