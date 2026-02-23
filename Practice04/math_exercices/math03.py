import math
pi = math.pi
sides = int(input("Input number of sides: " ))
len = int(input("Input the length of a side: "))
ctg_value = math.cos(pi/sides)/math.sin(pi/sides)
area = (sides*(pow(len,2)))/(4*ctg_value)
print(area)