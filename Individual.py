class Individual:
    fitness = 0
    bitString = ""
    probability = 0

    def __init__(self, fitness, bitString):
        self.fitness = fitness
        self.bitString = bitString

    def setProb(self, newProbability):
        self.probability = newProbability