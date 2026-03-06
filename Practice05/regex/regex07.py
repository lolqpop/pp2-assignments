import re

text = input("Enter string: ")

result = re.sub(r"_([a-z])", lambda x: x.group(1).upper(), text)
print(result)