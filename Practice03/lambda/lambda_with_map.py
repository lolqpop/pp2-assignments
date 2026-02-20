#1 example

numbers = [1, 2, 3, 4]
result = list(map(lambda x: x * 2, numbers))
print(result)  

#2 example

numbers = [2, 3, 4, 5]
squares = list(map(lambda x: x ** 2, numbers))
print(squares)  


#3 example

words = ["python", "code", "map"]
upper_words = list(map(lambda x: x.upper(), words))
print(upper_words)  

#4 example

words = ["hi", "hello", "python"]
lengths = list(map(lambda x: len(x), words))
print(lengths)  


