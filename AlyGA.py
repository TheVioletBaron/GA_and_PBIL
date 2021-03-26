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

    """Initiializing function for the GA class. Takes in a MAXSAT filename and variables specifying
    how to run a GA algorithim on it. Function is used to generate a GA object.
    """
    def __init__(self, file, popSize, select, cross_method, cross_prob, mut_prob, generations):
        self.file = file
        self.popSize = popSize
        self.select = select
        self.cross_method = cross_method
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob
        self.clauses = []
    
    """Function handle file reading on the MAXSAT problem, handling the first comment lines
    before obtaining the number of variables, clauses, and finally grabbing the clauses
    themselves and storing those in a list.
    """
    def readFile(self):
        f = open(self.file, "r")
        lines = f.readlines()
        while lines[0][0] == 'c':   #Remove beggining comment lines in file
            lines.remove(lines[0])

        first_line = lines[0].split() #Obtaining number of vairables and clauses 
        self.var_num = int(first_line[2])
        self.clause_num = int(first_line[3])
        lines.pop(0)
        self.clauses = lines

    """Function that generates an initial pool of Indivdual objects, each of which is assigned
    a random bitstring with a length equal to all others.
    """
    def generate_pool(self):
        for i in range(0, self.popSize):
            bitString = ""
            for j in range(0, self.var_num):
                new_bit = str(random.randrange(0, 2))
                bitString = bitString + new_bit
            newIndividual = Individual(0, bitString)
            self.solution_list.append(newIndividual)
        
        #self.evaluate_fitness(lines)
        for individual in self.solution_list:   #Determines the fitness of each Individual
            self.test_eval(self.clauses, individual)
    
    """Function that takes an individual solution and a given clause and checks
    if the solution satifies the clause. Returns a boolean.
    """
    def check_score(self, solution, clause):
        for literal in clause:
            good_value = "1" if int(literal) > 0  else "0"  
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
    
    """Given a set of problems and an Individual solution object, determines the fitness
    score of that Individual. Returns the updated fitness score as an int.
    """
    def test_eval(self, lines, individual):
        for line in lines:
            literals_list = line.split()
            if (self.check_score(individual, literals_list)):
                individual.fitness += 1
        return individual.fitness

    #defines that individuals should be sorted by fitness  THIS SEEMS STRANGE MAYBE?
    def rankSort(self, individual):
        return individual.fitness

    """Function that executes rank selection on the pool of solutions by first ranking
    them by their fitness scores, and then selecting based on rank-based probailities
    until a pool equal in size to the original population has been made.
    """
    def rankSelection(self):
        self.total_probability = 0
        
        self.solution_list.sort(key=self.rankSort)
        for i in range(0, len(self.solution_list)): #Calculating each Individual's probability
            self.solution_list[i].probability = (i + 1) / self.popSize
            self.total_probability += self.solution_list[i].probability
        # print("breeding pool")
        # for ind in self.solution_list:
            # print(str(ind.fitness) + " " + str(ind.probability) )
        self.select_breeding_pool()

    """Function that executes boltzmann selection by summing up all fitness scores
    as a denominator and then determining individual probabilities. Selection occurs
    until a pool equal in size to the original population has been made.
    """
    def boltzmann_selection(self):
        self.total_probability = 0
        #calculate denominator (sum of e to the fitness)
        denominator = 0
        for i in range(0, len(self.solution_list)):
            denominator += exp(self.solution_list[i].fitness)
        for i in range(0, len(self.solution_list)):
            self.solution_list[i].probability = exp(self.solution_list[i].fitness) / denominator
            self.total_probability += self.solution_list[i].probability
        self.select_breeding_pool()
    

    def exponential_rank_selection(self):
        self.total_probability = 0
        
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
        total_selected = 0
        selected = []
        while total_selected < self.popSize:
            rand = random.uniform(0, self.total_probability)
            selected_ind = self.get_selected_individual(rand)
            selected.append(selected_ind)
            total_selected += 1
        
        self.solution_list = []
        self.solution_list = selected
    
    def get_selected_individual(self, random_number):
        prob_so_far = 0
        prev_individual = 0
        for i in range(0, len(self.solution_list)):
            prob_so_far += self.solution_list[i].probability
            if prob_so_far > random_number:
                # total_selected += 1
                selected = self.solution_list[prev_individual]
                return (selected)
            prev_individual += 1
    
    def mutate(self):
        for individual in self.solution_list:
            for i in range (0, len(individual.bitString)):
                rand = random.random()
                if rand < self.mut_prob:
                    new_bit = "0" if individual.bitString[i] == "1" else "1"
                    individual.bitString = individual.bitString[:i] + new_bit + individual.bitString[i + 1:]
    
    #randomly choose parents, ensure they are two diff individuals
    def choose_parents(self):
        pos1 = random.randint(0, (len(self.solution_list) - 1))
        parent1 = self.solution_list[pos1]
        pos2 = random.randint(0, (len(self.solution_list) - 1))
        parent2 = self.solution_list[pos2]
        while parent1 == parent2:
            if len(self.solution_list) == 1:
                return parent1, parent1
            pos2 = random.randint(0, (len(self.solution_list) - 1))
            parent2 = self.solution_list[pos2]
        return parent1, parent2
        
    def crossover(self, cross_method):
        new_breeding_pool = []
        new_pop = 0
        while new_pop < self.popSize:
            if cross_method == "u":
                child1, child2 = self.uniform_crossover()
                new_breeding_pool.append(child1)
                new_breeding_pool.append(child2)
            else:
                child1, child2 = self.one_point_crossover()
                new_breeding_pool.append(child1)
                new_breeding_pool.append(child2)
            new_pop += 2
        self.solution_list = new_breeding_pool

    def uniform_crossover(self):
        parent1, parent2 = self.choose_parents()
        if (parent1 == parent2):
            print("oops")
        self.solution_list.remove(parent1)
        if parent1 != parent2:
            self.solution_list.remove(parent2)
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

        return child1, child2

    def one_point_crossover(self):
        parent1, parent2 = self.choose_parents()
        self.solution_list.remove(parent1)
        if parent1 != parent2:
            self.solution_list.remove(parent2)

        crossover_point = random.randint(1, self.var_num - 2) #don't choose last or first positions
        
        child1_string = parent1.bitString[0:crossover_point] + parent2.bitString[crossover_point:]
        child2_string = parent2.bitString[0:crossover_point] + parent1.bitString[crossover_point:]
        
        child1 = Individual(0, child1_string)
        child1.fitness = self.test_eval(self.clauses, child1)
        child2 = Individual(0, child2_string)
        child2.fitness = self.test_eval(self.clauses, child1)

        return child1, child2

    def get_best(self):
        max_solution =  self.solution_list[0]
        for individual in self.solution_list:
            if individual.fitness > max_solution.fitness:
                max_solution = individual
        return max_solution

    def convert_string(self, ex_solution):
        new_string = ""
        ex_solution = ex_solution.split()
        for num in ex_solution:
            if num != " ":
                if int(num) > 0:
                    new_string += "1"
                else:
                    new_string += "0"
        print("ex string")
        print(new_string)
        return new_string
    
    def compar_strings(self, string1, string2):
        diffs = 0
        for i in range (0, len(string1)):
            if string1[i] != string2[i]:
                diffs += 1
        diffs = diffs / len(string1)
        print("diffs: " + str(diffs))
        return diffs
    
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

    file_name = "t3pm3-5555.spn.cnf"
    file_name = "s3v80c1000-7.cnf"
    pop_size = 50
    select = "b"
    cross_method = "1p"
    cross_prob = 0.3
    mut_prob = 0.02
    iter_count = 25
    ga_or_pbil = "g"

    algo = GA(file_name, pop_size, select, cross_method, cross_prob, mut_prob, iter_count)
    algo.readFile()
    algo.generate_pool()
    gen_counter = 0

    # algo.one_point_crossover()
    
    while gen_counter < iter_count:
        print(algo.get_best().fitness)
        if select == "b":
            algo.boltzmann_selection()
        elif select == "r":
            algo.rankSelection()
        elif select == "er":
            algo.exponential_rank_selection()
       
        algo.crossover(cross_method)
        # if cross_method == "u":
        #     algo.uniform_crossover()
        # elif cross_method == "1p":
        #     algo.one_point_crossover()

        algo.mutate()
        gen_counter += 1
   
    
    best_indivdual = algo.get_best()
    print ("Best solution fitness is: " + str(best_indivdual.fitness))
    print ("Best solution bitstring is: " + best_indivdual.bitString)

    # new_string = algo.convert_string("1 2 -3 4 -5 -6 7 -8 -9 -10 -11 12 13 14 15 -16 -17 18 -19 20 21 22 -23 -24 25 26 -27 -28 -29 30 -31 -32 -33 34 35 36 37 38 39 -40 41 -42 -43 -44 45 -46 -47 48 -49 50 51 -52 53 -54 55 -56 57 58 -59 -60 61 62 63 -64 65 -66 -67 -68 69 70 71 -72 -73 74 -75 76 77 78 79 -80 ")
    # diffs = algo.compar_strings(new_string, best_indivdual.bitString)
    # test_fitness = algo.test_eval(algo.clauses, new_string)
    # print("test_fitness: " + str(test_fitness))

    
    

    
    
    


    
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
    
    
        







