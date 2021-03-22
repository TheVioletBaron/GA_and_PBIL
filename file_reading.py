import random
from Individual import Individual

test_file = "t3pm3-5555.spn.cnf"

f = open(test_file, "r")
lines = f.readlines()


#Removing comments
while lines[0][0] == 'c':
    lines.remove(lines[0])

var_num = 0
clause_num = 0

first_line = lines[0].split()
var_num = int(first_line[2])
clause_num = int(first_line[3])

#adding in the GA random solution generation code so we can do everything together

solution_count = 5
varible_count = var_num

count = 0
solution_list = []

for i in range(1, solution_count):
    bitString = ""
    for bit in range (0, varible_count):
        new_bit = str(random.randrange(0, 2))
        bitString = bitString + new_bit
    solution_list.append(Individual(-1, bitString))
print("solution list:")
print(solution_list)

#Method to compare a clause of literals with an indivudal solution bit string
def check_score(solution, clause):
    #print(clause)
    try:
        for literal in clause:
            positive_literal = int(literal) > 0 # check if literal j is positive or negative, maybe later jsut check if first char is - instead of casting
            good_value = "0"
            if (positive_literal):
                good_value = "1"
            if (solution.bitString[abs(int(literal)) - 1] != good_value):
                return False
    except:
        print("oh no")
        print(clause)
        print(solution)
        print("length" + str(len(solution.bitString)))
        print("")

    return True

# end random solution generator
for p in range(1, clause_num):
    line = lines[p]
    # print(line)
    literals_list = line.split() #  list of litersls
    for  i in range (0, len(solution_list)): # iterate through each individual i
        if (check_score(solution_list[i], literals_list)):
                #fitness[i] += 1
                solution_list[i].fitness += 1
 
# test_solution = "011"
# tett_clause = ["1", "2", "3"]
# print(check_score(test_solution, tett_clause))

print("individuals:")
for individual in solution_list:
    print(individual.bitString)
    print(individual.fitness)

#print("\nfitness:")
#print(fitness)


    


#Notes
#Double check that comments always come first
#Make sure we don't need comments....