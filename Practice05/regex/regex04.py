import re

text = input("Enter text: ")

pattern = r"[A-Z][a-z]+"
result = re.findall(pattern, text)
print(result)