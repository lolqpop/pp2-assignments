#1 example

a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a) 
'''
Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua.
'''
#2 example

b = "Hello, World!"
print(b[-5:-2]) #orl

#3 example

a = " Hello, World! "
print(a.strip()) # returns "Hello, World!"

#4 example

a = "Hello"
b = "World"
c = a + b
print(c) #HelloWorld

#5 example

age = 36
txt = f"My name is John, I am {age}"
print(txt) #My name is John, I am 36