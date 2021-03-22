#Aly and Jasper
import random
from Individual import Individual
from math import *

# solution_count = 10
# varible_count = 5

# count = 0
# solution_list = []

# for i in range(1, solution_count):
#     individual = ""
#     for bit in range (1, varible_count):
#         new_bit = str(random.randrange(0, 2))
#         individual = individual + new_bit
#     solution_list.append(individual)


# print (solution_list)

class GA(object):
    
    var_num = 0
    clause_num = 0
    solution_list = []
    total_probability = 0

    def __init__(self, file, popSize, select, cross_method, cross_prob, mut_prob, generations):
        self.file = file
        self.popSize = popSize
        self.select = select
        self.cross_method = cross_method
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob
    
    def readFile(self, test_file):
        test_file = "t3pm3-5555.spn.cnf"
        f = open(test_file, "r")
        lines = f.readlines()

        #Removing comments
        while lines[0][0] == 'c':
            lines.remove(lines[0])

        first_line = lines[0].split()
        self.var_num = int(first_line[2])
        self.clause_num = int(first_line[3])

        #adding in the GA random solution generation code so we can do everything together

        solution_count = 8
        varible_count = self.var_num

        count = 0

        for i in range(1, solution_count):
            bitString = ""
            for bit in range(0, varible_count):
                new_bit = str(random.randrange(0, 2))
                bitString = bitString + new_bit
            newIndividual = Individual(0, bitString)
            self.solution_list.append(newIndividual)
        
        self.evaluate_fitness(lines)
    
    #Method to compare a clause of literals with an indivudal solution bit string
    def check_score(self, solution, clause):
        for literal in clause:
            positive_literal = int(literal) > 0 # check if literal j is positive or negative, maybe later jsut check if first char is - instead of casting
            good_value = "0"
            if (positive_literal):
                good_value = "1"
            if (solution.bitString[abs(int(literal)) - 1] != good_value):
                return False
        return True
    
    #iterates through all lines in file and compares to each individual 
    def evaluate_fitness(self, lines):
        for p in range(1, self.clause_num):
            line = lines[p]
            literals_list = line.split() #  list of litersls
            for  i in range (0, len(self.solution_list)): # iterate through each individual i
                if (self.check_score(self.solution_list[i], literals_list)):
                    self.solution_list[i].fitness += 1
    
    def rankSort(self, individual):
        return individual.fitness

    def rankSelection(self):
        self.solution_list.sort(key=self.rankSort)
        #calculate probability for each ind
        for i in range(0, len(self.solution_list)):
            self.solution_list[i].probability = (i + 1) / self.popSize
            self.total_probability += self.solution_list[i].probability
        print("breeding pool")
        for ind in self.solution_list:
            print(str(ind.fitness) + " " + str(ind.probability) )
        self.select_breeding_pool()

    #calculate boltmann probabilites
    def boltzmann_selection(self):
        #calc denominator (sum of e to the fitness)
        denominator = 0
        for i in range(0, len(self.solution_list)):
            denominator += exp(self.solution_list[i].fitness)
        for i in range(0, len(self.solution_list)):
            self.solution_list[i].probability = exp(self.solution_list[i].fitness) / denominator
            self.total_probability += self.solution_list[i].probability
        
        self.select_breeding_pool()
    
    def exponential_rank_selection(self):
        self.solution_list.sort(key=self.rankSort)

        denominator = 0
        for i in range(0, len(self.solution_list)):
            denominator += exp(i)

        for i in range(0, len(self.solution_list)):
            self.solution_list[i].probability = exp(i) / denominator
            self.total_probability += self.solution_list[i].probability

        self.select_breeding_pool()

    #probabalistically select individuals
    def select_breeding_pool(self):
        prob_so_far = 0
        prev_individual = -1
        total_selected = 0
        selected = []
        while total_selected < self.popSize:
            rand = random.uniform(0, self.total_probability)
            print("rnd = " + str(rand))
            # for i in range(0, len(self.solution_list)):
            #     prob_so_far += self.solution_list[i].probability
            #     if prob_so_far > rand:
            #         total_selected += 1
            #         selected.append(self.solution_list[prev_individual])
            #         break;
            selected.append(self.get_selected_individual(rand))
            total_selected += 1
        print("selected")
        for ind in selected:
            print(ind.fitness)
        print("breeding pool")
        for ind in self.solution_list:
            print(str(ind.fitness) + " "  + str(ind.probability) )
    
    def get_selected_individual(self, random_number):
        prob_so_far = 0
        prev_individual = 0
        for i in range(0, len(self.solution_list)):
            prob_so_far += self.solution_list[i].probability
            if prob_so_far > random_number:
                # total_selected += 1
                return (self.solution_list[prev_individual])
            prev_individual += 1

def main():
        test_file = "t3pm3-5555.spn.cnf"
        algo = GA(test_file, 4, "1", "2", "3", "4", 5)
        algo.readFile(test_file)
        #algo.rankSelection()
        algo.boltzmann_selection()
        #algo.select_breeding_pool()

        # for ind in algo.solution_list:
        #     print(ind.fitness)

if __name__ == "__main__":
    main()   
    
    
        








