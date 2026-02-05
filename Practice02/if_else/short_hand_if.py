#1 example

age = 20
status = "Adult" if age >= 18 else "Minor"
print(status)

#2 example

is_logged_in = True
print("Welcome back!") if is_logged_in else print("Please log in.")

#3 example

num = 10
result = num * 2 if num % 2 == 0 else num
print(result)

#4 example

user_name = ""
display_name = user_name if user_name else "Guest"
print(display_name)

#5 example

score = 100
if score == 100: print("Perfect Score!")