# GA_and_PBIL
Authors: Jasper Gordon, Aly Hummel, Casey Edmonds-Estes, Mike Batal
The goal of this project is to use genetic algorithms (GA) and population-based incremental learning (PBIL)
to solve Maximum satisfiability problems (MAXSAT). Running this code requires that that the proper
MAXSAT files are saved to the same directory as these files (a folder should be included in the download).
To run this code, in terminal line you will need to type python3 Driver.py followed by 8 arguments on one single line. 
Those arguemnts include:

1. Algoirthm selection: g for GA or p for pbil
2. The name of your selected problem file
3. Desired population size (50 is a typical starting spot)
4. For pbil: learning rate for alpha best. For GA: Your desired selection method (r = rank, er = exponential rank,
b = boltzman)
5. For pbil: learning rate for alpha worst. For GA: Your desired crossover method (u = uniform, 1p = 1-point)
6. Mutation probability
7. For pbil: mutation amount. For GA: The crossover probability (0.7 is typical starting spot)
8. Desired number of iterations (start with 100)


After placing each of those arugments after python3 Driver.py all in one line seperated by spaces,
press enter and you should soon see outputs with the results.

Example arugment line: python3 Driver.py g t3pm3-5555.spn.cnf 50 r 1p .01 .7 100