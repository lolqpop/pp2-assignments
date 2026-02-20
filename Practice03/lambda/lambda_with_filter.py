#1 example

nums = [1,2,3,4,5,6,7,8,9]
evens = list(filter(lambda a : a % 2 == 0, nums))
print(*evens)

#2 example

words = ["cat", "apple", "hi", "banana"]
long_words = list(filter(lambda x: len(x) > 3, words))
print(long_words)  

#3 example

numbers = [-5, 3, 0, -2, 8]
posnum = list(filter(lambda x: x > 0, numbers))
print(posnum)  

#4 exmaple

