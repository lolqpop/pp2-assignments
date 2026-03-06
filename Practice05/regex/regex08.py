import re

text = input("Enter text: ")

result = re.split(r"(?=[A-Z])", text)
print(result)