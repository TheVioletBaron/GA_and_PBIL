from PBIL import Pbil
from GA import GA
import sys
import math

'''
Driver contains a main method which creates a GA object and a PBIL object.
Those then run their respective programs and output their results, times, etc.
Driver then formats/prints/saves those outputs as needed.
'''

def argumentError():
	print("Please format the arguments as per the assignment sheet.")
	sys.exit(0)

def main():
	ga_or_pbil = sys.argv[1]
	problem_file = sys.argv[2]
	pop_size = sys.argv[3]
	pos_lr = sys.argv[4] #for GA this is the selection method
	neg_lr = sys.argv[5] #for GA this is the crossover method
	mut_prob = sys.argv[6]
	mut_amnt = sys.argv[7] #for GA this is the crossover probability
	iter_cnt = sys.argv[8]
	
	if (ga_or_pbil == "g"):
		g = GA(problem_file, pop_size, pos_lr, neg_lr, mut_prob, mut_amnt, iter_cnt)
		g.runner() #GA method that handles running and output
		
	elif (ga_or_pbil == "p"):
		p = Pbil(problem_file, pop_size, pos_lr, neg_lr, mut_prob, mut_amnt, iter_cnt)
		print("File name: " + problem_file)
		print("Variable count: " + str(p.length))
		print("Clause count: " + str(p.max_fit))
		print("Clauses satisfied: " + str(p.final_count))
		print("Percentage satsified: " + str(round(p.final_count/p.max_fit*100, 2)))
		print("Satisfying assignment: " + str(p.best))
		print("Iteration found: " + str(p.final_iter))
	else:
		argumentError()
	

if __name__ == '__main__':
    main()
