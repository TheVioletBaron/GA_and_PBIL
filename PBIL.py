import re
import random
'''
Population Based Incremental Learning

  Parameters
        ----------
        
        file : str
            The name of a file containing a MAXSAT problem in conjunctive normal form
        popSize : int
            The size of the population generated during each iteration
        alphaBest : float
            The learning rate when updating the probability vector with the best individuals
        alphaWorst : float
            The learning rate when updating the probability vector with the worst individuals
        mProb : float
            The mutation probability
        mShift : float
            The mutation amount
        iters : int
            The maximum number of iterations
'''

class Pbil(object):
    
    def __init__(self, file, popSize, alphaBest, alphaWorst, mProb, mShift, iters):
        """
        """
        
        self.file = file
        self.popSize = int(popSize)
        self.alphaBest = alphaBest
        self.alphaWorst = alphaWorst
        self.mProb = mProb
        self.mShift = mShift
        self.iters = int(iters)
        cnf = open(self.file)
        lines = cnf.readlines()
        length = 0
        for line in lines:
                has = re.match("(-?[0-9]+| )+", line)
                if (has):
                       length = len(has.group().split())
                       break
        pv = [0.5] * length

        samples = []
        while self.iters:
                while len(samples) < self.popSize:
                        print("f")
                        sample = []
                        for i in pv:
                                if (random.random() > i):
                                        sample.append(0)
                                else:
                                        sample.append(1)
                        samples.append(sample)
                self.iters = self.iters - 1

	#store Probability Vector as probVec List
	#for sample in samples
	#bestvec
	#worstvec
	#update toward
	#update away
	#mutate




        
    def evaluate_fitness(individual):
        cnf = open(self.file)
        fitness = 0
        Lines = f.readlines()
        
        # TODO: Add loop to iterate through lines until the "p cnf \d \d" line is found
        
        for line in Lines:
            line = line.strip()
            clause = line.split()
            index = 0
            while(clause[index] != "0"):
               #While loop takes the variables in each clause, finds the corresponding variable in the individual, and
               #compares the two to update the fitness accordingly
                variable = individual[abs(int(clause[index]))-1] #Take absolute value of to find index of variable in individual
                if(variable == 1 and int(clause[index])>0):
                    fitness += 1
                elif(variable == 0 and int(clause[index])<0):
                    fitness += 1
                index += 1
        return fitness
