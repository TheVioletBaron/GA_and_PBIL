#Aly and Jasper
import random
from Individual import Individual
from math import *
import sys
import time

class GA(object):
    
    var_num = 0
    clause_num = 0
    solution_list = []
    total_probability = 0
    clauses = []

    """Initiializing function for the GA class. Takes in a MAXSAT filename and variables specifying
    how to run a GA algorithim on it. Function is used to generate a GA object.
    """
    def __init__(self, file, popSize, select, cross_method, mut_prob, cross_prob, generations):
        self.file = file
        self.popSize = popSize
        self.select = select
        self.cross_method = cross_method
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob
        self.clauses = []
        self.sum_of_ranks = 0


        
    
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
    
    """Function that takes an Individual solution and a given clause and checks
    if the solution satifies the clause. Returns a boolean.
    """
    def check_score(self, solution, clause):
        for literal in clause[:-1]: #Needs to ignore the 0 at the end of each clause
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
    def rank_selection(self):
        self.total_probability = 0
        self.solution_list.sort(key=self.rankSort)
    
        for i in range(0, len(self.solution_list)): #Calculating each Individual's probability
            self.solution_list[i].probability = (i + 1) / self.sum_of_ranks
            self.total_probability += self.solution_list[i].probability
        self.select_breeding_pool()

    """Executes boltzmann selection by summing up all fitness scores
    as a denominator and then determining each Individual's probability. Selection occurs
    until a pool equal in size to the original population has been made.
    """
    def boltzmann_selection(self):
        self.total_probability = 0
        for i in range(0, len(self.solution_list)): #Calculating each Individual's probability
            self.solution_list[i].probability = exp(self.solution_list[i].fitness) / self.sum_of_ranks
            self.total_probability += self.solution_list[i].probability
        self.select_breeding_pool()
    

    """Executes exponential rank selection, calculating an indvidual's probability of
    being selected by taking e to the power of the individual's rank, and dividing
    that by the sum of e to the power of all the Inviduals' ranks. Calls method to
    do the actual selection.
    """
    def exponential_rank_selection(self):
        self.total_probability = 0
        self.solution_list.sort(key=self.rankSort)
        for j in range(0, len(self.solution_list)):
            self.solution_list[j].probability = exp(j) / self.sum_of_ranks
            self.total_probability += self.solution_list[j].probability

        self.select_breeding_pool()

    """Probabilistically selects Individuals and places them into the breeding
    pool until the pool is full i.e. equal to the size of the original population.
    Calculates a random float value which is used to find each Individual.
    """
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
    
    """Given a random float value between 0 and the total of all the Individual
    probabilities calculated above, selects the indvidual who matches the random value.
    Returns an Individual object.
    """
    def get_selected_individual(self, random_number):
        prob_so_far = 0 #holds cumulative probabilties
        prev_individual = 0
        for i in range(0, len(self.solution_list)):
            prob_so_far += self.solution_list[i].probability
            if prob_so_far > random_number:
                # total_selected += 1
                #selected = self.solution_list[prev_individual] #this still confuses me, seems like it should be that one that passed
                return (self.solution_list[i])
            prev_individual += 1
    
    """Iterates through the Individual solutions and probabilistically mutates on a randomly
    selected bit in the Individual's bitstring.
    """
    def mutate(self):
        for individual in self.solution_list:
            for i in range (0, len(individual.bitString)):
                rand = random.random()
                if rand < self.mut_prob:
                    new_bit = "0" if individual.bitString[i] == "1" else "1"
                    individual.bitString = individual.bitString[:i] + new_bit + individual.bitString[i + 1:]
    
    #randomly choose parents, ensure they are two diff individuals
    """To help with crossing over, randomly selects two Individuals from the solution
    list, ensuring that they are different, and then returns the Individual objects.
    """
    def choose_parents(self):
        pos1 = random.randint(0, (len(self.solution_list) - 1))
        parent1 = self.solution_list[pos1]
        pos2 = random.randint(0, (len(self.solution_list) - 1))
        parent2 = self.solution_list[pos2]
        while pos2 == pos1:
        #while parent1 == parent2: #If parents are the same object, finds a new second parent
            if len(self.solution_list) == 1:
                return parent1, parent1
            pos2 = random.randint(0, (len(self.solution_list) - 1))
            parent2 = self.solution_list[pos2]
        return parent1, parent2

    """Given a string representing a crossover method as an argument, crosses over
    until a new breeding pool of the correct size i.e. the original population
    size is achieved. Depending on the crossover method provided, makes a
    function call to aquire those two children to add.
    """    
    def crossover(self, cross_method):
        new_breeding_pool = []
        new_pop = 0
        while new_pop < self.popSize:
            if cross_method == "u": #uniform crossover
                child1, child2 = self.uniform_crossover()
                new_breeding_pool.append(child1)
                new_breeding_pool.append(child2)
            else:   #1-point crossover
                child1, child2 = self.one_point_crossover()
                new_breeding_pool.append(child1)
                new_breeding_pool.append(child2)
            new_pop += 2
        self.solution_list = new_breeding_pool

    """Performs uniform crossover by aquriing two parent Individual objects, and then 
    randomly decciding for each variable randomly choosing which parent to take from.
    Returns the children as Individual objects with new fitnesses and bitstrings.
    """
    def uniform_crossover(self):
        parent1, parent2 = self.choose_parents()
        # if (parent1 == parent2):
        #     print("oops")
        # print("parent1 before removal: " + parent1.bitString)
        self.solution_list.remove(parent1)
        if parent1 != parent2:
            self.solution_list.remove(parent2)
        # print("parent 1 after removal: " + parent1.bitString)
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
        child2.fitness = self.test_eval(self.clauses, child2)
        return child1, child2

    """Performs one-point crossover, choosing two parents, randomly selecting a crossover
    point that does not include the first or last variables of a bitstring, and then
    crosses over between the two parents at that point (swaps bitstrings after the
    stated point). Returns two child Individual objects.
    """
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
        child2.fitness = self.test_eval(self.clauses, child2)
        return child1, child2

    """Iterates through the solution list and returns the Individual object
    with the maximum fitness score.
    """
    def get_best(self):
        max_solution = self.solution_list[0]
        for individual in self.solution_list:
            if individual.fitness > max_solution.fitness:
                max_solution = individual
        return max_solution

    """Helper method that converts a given solution string (ex: 1 -2 3 -4 -5 -6 7 etc...)
    into a bitstring. Returns a bitstring.
    """
    def convert_string(self, ex_solution):
        new_string = ""
        ex_solution = ex_solution.split()
        for num in ex_solution:
            if num != " ":
                if int(num) > 0:
                    new_string += "1"
                else:
                    new_string += "0"
        return new_string
    
    """Helper method that converts a given bitstring into a solution string 
    (ex: 1 -2 3 -4 -5 -6 7 etc...). Returns the solution string.
    """
    def convert_string_to_vars(self, bitstring):
        new_string = ""
        var_counter = 1
        for char in bitstring:
            if char == '1':
                new_string += str(var_counter)

            else:
                new_string += "-"
                new_string += str(var_counter)
            var_counter += 1
            new_string += " "
        return new_string

    """Helper method that compares two bitstrings and returns the number of differences
    between them as an int value.
    """
    def compar_strings(self, string1, string2):
        diffs = 0
        for i in range (0, len(string1)):
            if string1[i] != string2[i]:
                diffs += 1
        diffs = diffs / len(string1)
        print("diffs: " + str(diffs))
        return diffs

    """A seperate attempt to consolidate the selection, crossover, and mutation all in one function.
    Instead of calling each one at a time on the entire population, this method selects two
    parent solutions, crosses over, mutates, and adds the new solutions to the breeding pool,
    repeating until the population size is complete.
    """
    def rank2(self):
        new_pool = []
        self.solution_list.sort(key=self.rankSort) #Sorting the solution list
        rankList = [0] * self.popSize #Begin Selection
        for i in range(0, self.popSize): 
                rankList[i] = self.popSize - i #Creates decending rank values [100,99,98,...]
                if i != 0:
                    rankList[i] += rankList[i-1] #Sums elemnts of array for Rank selection [100, 199, 197,...]
        while(len(new_pool) < self.popSize): 
            rand = random.uniform(1, rankList[-1]) #Random float between 1 and sum of ranks
            for i in range(0, self.popSize):
                if rankList[i] > rand: #Probabilistically selects solution
                    parent1 = self.solution_list[i]
                    break
            parent2 = parent1 
            while(parent2 == parent1): #Ensuring parent 2 is not equal to parent 1
                rand2 = random.uniform(1, rankList[-1])
                for i in range(0, self.popSize):
                    if rankList[i] > rand2:
                        parent2 = self.solution_list[i]
                        break
            crossover_point = random.randint(1, self.var_num - 2) #1-point crossover
            child1_string = parent1.bitString[0:crossover_point] + parent2.bitString[crossover_point:]
            child2_string = parent2.bitString[0:crossover_point] + parent1.bitString[crossover_point:]
            child1 = Individual(0, child1_string) 
            child2 = Individual(0, child2_string)
            children = [child1, child2] 
            for individual in children:
                for i in range (0, len(individual.bitString)): #Mutation
                    rand = random.random()
                    if rand <= self.mut_prob:
                        new_bit = "0" if individual.bitString[i] == "1" else "1"
                        individual.bitString = individual.bitString[:i] + new_bit + individual.bitString[i + 1:]
            child2.fitness = self.test_eval(self.clauses, child2)
            child1.fitness = self.test_eval(self.clauses, child1)
            new_pool.append(child1)
            new_pool.append(child2)
        self.solution_list = new_pool 
            
            
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

    #file_name = "t3pm3-5555.spn.cnf"
    file_name = "s3v80c1000-7.cnf"
    pop_size = 30
    select = "b" 
    cross_method = "u"
    cross_prob = 0.7
    mut_prob = 0.04
    iter_count = 1000
    ga_or_pbil = "g"
    bestInd = Individual(0, '1') 
    iterFound = 0

    start_time = int(round(time.time()) * 1000)
    algo = GA(file_name, pop_size, select, cross_method, cross_prob, mut_prob, iter_count)
    algo.readFile()
    algo.generate_pool()
    gen_counter = 0

    while gen_counter < iter_count:
        #Calling selection
        if select == "b":
            for i in range (0, algo.popSize + 1): #Summing up total of ranks for later use
                algo.sum_of_ranks += exp(algo.solution_list[i - 1].fitness)
            algo.boltzmann_selection()
        elif select == "r":
            for i in range (0, algo.popSize + 1): #Summing up total of ranks for later use
                algo.sum_of_ranks += i
            algo.rank_selection()
        elif select == "er":
            for i in range (0, algo.popSize + 1): #Summing up total of ranks for later use
                algo.sum_of_ranks += exp(i)
            algo.exponential_rank_selection()
        algo.crossover(cross_method)
        algo.mutate()

        best_of_gen = algo.get_best()
        if best_of_gen.fitness > bestInd.fitness:
            bestInd = best_of_gen
            print("new best found")
            print(best_of_gen.fitness)
            iterFound = gen_counter
        gen_counter += 1
        if gen_counter % 200 == 0:
            print (str(gen_counter))
            print (str(bestInd.fitness))
    end_time = int(round(time.time()) * 1000)
    complete_percentage = (bestInd.fitness / algo.clause_num) * 100
    best_string = algo.convert_string_to_vars(bestInd.bitString)
    
    print ("Filename:" + file_name)
    print ("Total number of variables/clauses possible: " + str(algo.var_num) + "/" + str(algo.clause_num))
    print ("Number of clauses satisfied: " + str(bestInd.fitness) + " or " + str(complete_percentage) + "%")
    print ("Best solution: " + best_string)
    print ("Iteration when optimal solution found: " + str(iterFound))
    print ("Test Duration = " + str(end_time - start_time))
    print ("Best bitstring: " + bestInd.bitString)

if __name__ == "__main__":
    main()   
    
    
        








