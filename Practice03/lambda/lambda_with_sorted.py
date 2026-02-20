#1 example

numbers = [5, 2, 9, 1, 7]
result = sorted(numbers)
print(result)  

#2 example

numbers = [5, 2, 9, 1, 7]
result = sorted(numbers, key=lambda x: -x)
print(result) 

#3 example

words = ["cat", "banana", "hi", "apple"]
result = sorted(words, key=lambda x: len(x))
print(result)  

#4 example

students = [("Alex", 85), ("Bob", 92), ("Carl", 78)]
result = sorted(students, key=lambda x: x[1])
print(result)
