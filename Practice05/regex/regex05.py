import re

text = input("Enter string: ")

pattern = r"a.*b$"
if re.search(pattern, text):
    print("Yes")
else:
    print("No")