
with open("ex.txt", "a") as file:
    file.write("Exampleee\n")


with open("ex.txt", "r") as file:
    print(file.read())