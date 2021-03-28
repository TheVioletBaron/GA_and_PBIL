
import re
import random
import math
import time
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
    
        #Fixed, previous version was returning low fitness
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
                clause = line.strip().split()
                passed = True
                for cv in clause[:-1]: #changed so Ignores 0
                        sv = individual[abs(int(cv)) - 1]
                        if sv == 0 and int(cv) > 0:
                                passed = False
                        if sv == 1 and int(cv) < 0:
                                passed = False
                if passed:
                        fitness = fitness + 1
        return fitness #Fitness is always returned correctly when using TestProb.cnf


    def __init__(self, file, popSize, alphaBest, alphaWorst, mProb, mShift, iters):
        """
        """
        start_time = int(round(time.time()*1000))
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
        max_fit = 0
        print("Number of iterations: " + str(self.iters))
        print("Population size: " + str(self.popSize))
        for line in lines:
                has = re.search("[0-9]+[ ]+[0-9]+", line)
                if (has):
                       length = int(has.group().split()[0])
                       max_fit = int(has.group().split()[1])
                       break
        pv = [0.5] * length
        samples = []
        best_fit = 0
        worst_fit = max_fit + 1
        best = []
        worst = []
        max_iters = self.iters
        while self.iters:
                while len(samples) < self.popSize: #building correct number of samples
                        sample = []
                        for i in pv:
                                if (random.random() > i): #Changed: to > because probability in pv is for bit being 1? 
                                        sample.append(0)
                                else:
                                        sample.append(1)
                        samples.append(sample)
                best_fit = 0
                worst_fit = max_fit + 1
                best = []
                worst = []
                for sample in samples:
                        #Edited to test evalFitness()
                        #sample = [1, 1, 0, 0, 0, 1, 0, 1, 0] #testing with TestProb.cnf should have fitness of 1 but gets 0

                        s_fit = self.evaluate_fitness(sample)
                        if s_fit >= best_fit:
                                if s_fit == best_fit:
                                        if random.random() > 0.5:
                                                best_fit = s_fit
                                                best = sample
                                else:
                                        best_fit = s_fit
                                        best = sample
                        if s_fit <= worst_fit:
                                if s_fit == worst_fit:
                                        if random.random() > 0.5:
                                                worst_fit = s_fit
                                                worst = sample
                                else:
                                        worst_fit = s_fit
                                        worst = sample
                for i in range(length):
                        pv[i] = pv[i]*(1 - self.alphaBest) + best[i] * self.alphaBest #pv appears to be being updated too 
                for i in range(length):
                        if best[i] != worst[i]:
                                pv[i] = pv[i]*(1 - self.alphaWorst) - worst[i] * self.alphaWorst
                #print(pv)
                i = 0
                while(i < len(pv)): #Mutation
                        if(random.random() < self.mProb):
                                if(random.random() < 0.5):
                                        pv[i] = pv[i] * (1 - self.mShift)
                                else:
                                        pv[i] = pv[i] * (1 - self.mShift) + self.mShift
                        i += 1
                samples = []
                #print(self.iters)
                self.iters = self.iters - 1
                if (self.evaluate_fitness(best) == max_fit):
                        break

        #print(pv)
        end_time = int(round(time.time()*1000))
        print("Test duration: " + str(end_time - start_time))
        self.final_iter = max_iters - self.iters
        self.final_count = self.evaluate_fitness(best)
        self.best = best
        self.max_fit = max_fit
        self.length = length


