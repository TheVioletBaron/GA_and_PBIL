#!/bin/bash

# Testing for GA
#filename = "s3v80c1000-7.cnf"
#baseline selection method: b
#baseline topology: ri
#baseline mut prob: 0.25

echo "GA TESTING"
for pop in 16 30 64 
do
    for iter {0...10}
    do
        python3 Driver.py g s3v80c1000-7.cnf ${pop} b 1p 0.01 0.7 5000
    done
done

#echo "MUTATION TESTING"
#for prob in 0.01 0.1 0.25 0.5 #mut prob 
#do
#    for pop in 16 30 64 
#    do
#        python3 interface.py s3v80c1000-7.cnf ${pop} "ri" "b" ${prob}
#    done
#done