#!/bin/bash
# file1 = "t3pm3-5555.spn.cnf"
# file2 = "s3v80c1000-7.cnf"

#TODO decide on final files that match up with GA

# general testing for GA
for file in "t3pm3-5555.spn.cnf" "HG-3SAT-V250-C1000-7.cnf" "s3v80c1000-7.cnf"
do
    for pop in 10 50 100 500 1000 
    do
        for it_count in 10 50 100 500 1000 
        do
            python3 Driver.py g ${file} ${pop} b 1p 0.02 0.7 ${it_count}

        done
    done
done




