#Aly and Jasper
import random
from Individual import Individual
from math import *
import sys

class GA(object):
    
    var_num = 0
    clause_num = 0
    solution_list = []
    total_probability = 0
    clauses = []

    def __init__(self, file, popSize, select, cross_method, cross_prob, mut_prob, generations):
        self.file = file
        self.popSize = popSize
        self.select = select
        self.cross_method = cross_method
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob
        self.clauses = []
    
    def readFile(self):
        f = open(self.file, "r")
        lines = f.readlines()
        #Removing comments
        while lines[0][0] == 'c':
            lines.remove(lines[0])

        first_line = lines[0].split()
        self.var_num = int(first_line[2])
        self.clause_num = int(first_line[3])
        lines.pop(0)
        self.clauses = lines

        #adding in the GA random solution generation code so we can do everything together

    def generate_pool(self):
        for i in range(1, self.popSize):
            bitString = ""
            for j in range(0, self.var_num):
                new_bit = str(random.randrange(0, 2))
                bitString = bitString + new_bit
            newIndividual = Individual(0, bitString)
            self.solution_list.append(newIndividual)
        
        #self.evaluate_fitness(lines)
        for individual in self.solution_list:
            self.test_eval(self.clauses, individual)
    
    #Compare a clause of literals with an indivudal solution bit string
    def check_score(self, solution, clause):
        for literal in clause:
            good_value = "0" if int(literal) > 0  else "1"#  check if literal j is positive or negative, maybe later jsut check if first char is - instead of casting
            if (solution.bitString[abs(int(literal)) - 1] != good_value):
                return False
        return True
    
    #iterates through all lines in file and compares to each individual 
    # def evaluate_fitness(self, lines):
    #     for p in range(1, self.clause_num):
    #         line = lines[p]
    #         literals_list = line.split() #  list of litersls
    #         for  i in range (0, len(self.solution_list)): # iterate through each individual i
    #             if (self.check_score(self.solution_list[i], literals_list)):
    #                 self.solution_list[i].fitness += 1
    
    #checks by individual what fitness is -- makes crossover easier
    def test_eval(self, lines, individual):
        for line in lines:
            literals_list = line.split() #  list of litersls
            if (self.check_score(individual, literals_list)):
                individual.fitness += 1
        return individual.fitness

    #defines that individuals should be sorted by fitness
    def rankSort(self, individual):
        return individual.fitness

    def rankSelection(self):
        self.solution_list.sort(key=self.rankSort)
        #calculate probability for each ind
        for i in range(0, len(self.solution_list)):
            self.solution_list[i].probability = (i + 1) / self.popSize
            self.total_probability += self.solution_list[i].probability
        # print("breeding pool")
        # for ind in self.solution_list:
            # print(str(ind.fitness) + " " + str(ind.probability) )
        self.select_breeding_pool()

    #calculate boltmann probabilites
    def boltzmann_selection(self):
        #calculate denominator (sum of e to the fitness)
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
    
    def mutate(self):
        for individual in self.solution_list:
            for i in range (0, len(individual.bitString)):
                rand = random.random()
                if rand > self.mut_prob:
                    new_bit = "0" if individual.bitString[i] == "1" else "1"
                    individual.bitString = individual.bitString[:i] + new_bit + individual.bitString[i + 1:]
    
    #randomly choose parents, ensure they are two diff individuals
    def choose_parents(self):
        pos1 = random.randint(0,2)
        pos1 = random.randint(0, (len(self.solution_list) - 1))
        parent1 = self.solution_list[pos1]
        pos2 = random.randint(0, (len(self.solution_list) - 1))
        while pos2 == pos1 and len(self.solution_list) > 1:
            pos2 = random.randint(0, (len(self.solution_list) - 1))
        parent2 = self.solution_list[pos2]
        return parent1, parent2

    def uniform_crossover(self):
        parent1, parent2 = self.choose_parents()
        print(parent1.bitString)
        print(parent2.bitString)
        child1_string = ""
        child2_string= ""
        for i in range (0, self.var_num):
            rand = random.randint(0, 1)
            if rand == 0:
                child1_string = child1_string + parent1.bitString[i]
                child2_string = child2_string + parent2.bitString[i]
            else:
                child1_string = child1_string + parent2.bitString[i]
                child2_string = child2_string + parent1.bitString[i]
        
        child1 = Individual(0, child1_string)
        child1.fitness = self.test_eval(self.clauses, child1)
        child2 = Individual(0, child2_string)
        child2.fitness = self.test_eval(self.clauses, child1)
        print(child1.bitString)
        print(child2.bitString)
        return child1, child2

    def one_point_crossover(self):
        parent1, parent2 = self.choose_parents()

        print(parent1.bitString)
        print(parent2.bitString)

        crossover_point = random.randint(1, (len(self.var_num) - 2)) #don't choose last or first positions
        print(crossover_point)

        child1_string = parent1.bitString[0:crossover_point] + parent2.bitString[crossover_point + 1:]
        child2_string = parent2.bitString[0:crossover_point] + parent1.bitString[crossover_point + 1:]

        child1 = Individual(0, child1_string)
        child1.fitness = self.test_eval(self.clauses, child1)
        child2 = Individual(0, child2_string)
        child2.fitness = self.test_eval(self.clauses, child1)

        print(child1.bitString)
        print(child2.bitString)
        return child1, child2

    def get_best(self):
        max_solution =  self.solution_list[0]
        for individual in self.solution_list:
            if individual.fitness > max_solution.fitness:
                max_solution = individual
        return max_solution
    
def main():
    '''
    file_name = sys.argv[1]
    pop_size = int(sys.argv[2])
    select = sys.argv[3]
    cross_method = sys.argv[4]
    cross_prob = float(sys.argv[5])
    mut_prob = float(sys.argv[6])
    iter_count = int(sys.argv[7])
    ga_or_pbil = sys.argv[8]
    '''

    file_name = "HG-3SAT-V250-C1000-7.cnf"
    pop_size = 50
    select = "b"
    cross_method = "u"
    cross_prob = 0.75
    mut_prob = 0.001
    iter_count = 20
    ga_or_pbil = "g"

    algo = GA(file_name, pop_size, select, cross_method, cross_prob, mut_prob, iter_count)
    algo.readFile()
    algo.generate_pool()

    gen_counter = 0
    while gen_counter < iter_count:
        if select == "b":
            algo.boltzmann_selection()
        elif select == "r":
            algo.rankSelection()
        elif select == "er":
            algo.exponential_rank_selection()

        if cross_method == "u":
            algo.uniform_crossover()
        elif cross_method == "1p":
            algo.one_point_crossover()

        algo.mutate()
        gen_counter += 1
    
    best_indivdual = algo.get_best()
    print ("Best solution fitness is: " + str(best_indivdual.fitness))
    print ("Best solution bitstring is: " + best_indivdual.bitString)


    
    

    
    
    


    
    '''
    test_file = "HG-3SAT-V250-C1000-7.cnf "
    
    algo.readFile()
    #algo.rankSelection()
    #algo.boltzmann_selection()
    #algo.select_breeding_pool()
    test = Individual(2, "000")
    test2 = Individual(2, "111")
    algo.solution_list.append(test)
    algo.solution_list.append(test2)
    # algo.flip_bit(test, 0)
    # print(test.bitString)

    # algo.flip_bit(test, 1)
    # print(test.bitString)

    # algo.flip_bit(test, 2)
    # print(test.bitString)

    algo.uniform_crossover()

    # for ind in algo.solution_list:
    #     print(ind.fitness)
    
    '''

if __name__ == "__main__":
    main()   
    
    
        








