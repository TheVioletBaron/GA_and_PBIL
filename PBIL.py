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
    

    def evaluate_fitness(self, individual):
        cnf = open(self.file)
        fitness = 0
        lines = cnf.readlines()
        start_index = 0
        for line in lines:
                has = re.match("(-?[0-9]+| )+", line)
                if (has):
                        break
                start_index = start_index + 1
        lines = lines[start_index:]
        for line in lines:
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


    def __init__(self, file, popSize, alphaBest, alphaWorst, mProb, mShift, iters):
        """
        """
        
        self.file = file
        self.popSize = int(popSize)
        self.alphaBest = float(alphaBest)
        self.alphaWorst = float(alphaWorst)
        self.mProb = float(mProb)
        self.mShift = float(mShift)
        self.iters = int(iters)
        cnf = open(self.file)
        lines = cnf.readlines()
        length = 0
        for line in lines:
                has = re.search("[0-9]+", line)
                if (has):
                       length = int(has.group().split()[0])
                       break
        pv = [0.5] * length
        print(length)
        samples = []
        while self.iters:
                while len(samples) < self.popSize:
                        sample = []
                        for i in pv:
                                if (random.random() > i):
                                        sample.append(0)
                                else:
                                        sample.append(1)
                        samples.append(sample)
                best_fit = 0
                worst_fit = length
                best = []
                worst = []
                for sample in samples:
                        s_fit = self.evaluate_fitness(sample)
                        if s_fit > best_fit:
                                best_fit = s_fit
                                best = sample
                        if s_fit < worst_fit:
                                worst_fit = s_fit
                                worst = sample
                for i in range(length):
                        pv[i] = pv[i]*(1 - self.alphaBest) + best[i] * self.alphaBest
                for i in range(length):
                        if best[i] != worst[i]:
                                pv[i] = pv[i]*(1 - self.alphaWorst) + worst[i] * self.alphaWorst
	#mutate
                self.iters = self.iters - 1



