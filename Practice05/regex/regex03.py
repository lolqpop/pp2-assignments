import re

text = input("Enter text: ")

pattern = r"[a-z]+_[a-z]+"
result = re.findall(pattern, text)
print(result)