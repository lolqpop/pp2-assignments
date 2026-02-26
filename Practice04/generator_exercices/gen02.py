n = int(input("Input your number: ")) 

even_lst = (x  for x in range(n) if x%2 ==0)

print(list(even_lst))