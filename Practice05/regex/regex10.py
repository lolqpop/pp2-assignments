import re

text = input("Enter a string: ")

result = re.sub(r"([A-Z])", r"_\1", text).lower()
print(result)