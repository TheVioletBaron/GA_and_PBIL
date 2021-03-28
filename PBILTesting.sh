#!/bin/bash
file1 = "t3pm3-5555.spn.cnf"
file2 = "s3v80c1000-7.cnf"
for file in "t3pm3-5555.spn.cnf" "s3v80c1000-7.cnf" "HG-3SAT-V250-C1000-7.cnf"
do
    for pop in 10 50 100 500 1000 
    do
        for it_count in 10 50 100 500 1000 
        do
            python3 Driver.py p ${file} ${pop} 0.05 0.025 0.02 0.05 ${it_count}
        done
    done
done
