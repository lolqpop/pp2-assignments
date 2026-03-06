import re

text = input("Enter a string: ")

pattern = r"ab*"

if re.fullmatch(pattern, text):
    print("Yes")
else:
    print("No ")