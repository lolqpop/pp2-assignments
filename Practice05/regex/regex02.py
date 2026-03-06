import re

text = input("Enter string: ")

pattern = r"ab{2,3}"

if re.fullmatch(pattern, text):
    print("Yes")
else:
    print("No")