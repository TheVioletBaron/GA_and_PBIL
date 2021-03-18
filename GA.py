#Aly and Jasper
import random


solution_count = 10
varible_count = 5

count = 0
solution_list = []

for i in range(1, solution_count):
    individual = ""
    for bit in range (1, varible_count):
        new_bit = str(random.randrange(0, 2))
        individual = individual + new_bit
    solution_list.append(individual)


print (solution_list)








