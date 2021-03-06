import PBIL.py as PBIL
import GA.py as GA
import sys

'''
Driver contains a main method which creates a GA object and a PBIL object.
Those then run their respective programs and output their results, times, etc.
Driver then formats/prints/saves those outputs as needed.
'''

def argumentError():
	print("Please format the arguments as per the assignment sheet.")
	sys.exit(0)

def main():
	problem_file = sys.argv[1]
	individuals_per_iter = sys.argv[2]
	pos_lr = sys.argv[3]
	neg_lr = sys.argv[4]
	mut_prob = sys.argv[5]
	mut_amnt = sys.argv[6]
	iter_cnt = sys.arv[7]
	ga_or_pbil = sys.argv[8]
	
	if (ga_or_pbil == "g"):
		g = GA()
	elif (ga_or_pbil == "p"):
		p = PBIL(problem_file, individuals_per_iter, pos_lr, neg_lr, mut_prob, mut_amnt, iter_cnt)
	else:
		argumentError()
	

if __name__ == '__main__':
    main()