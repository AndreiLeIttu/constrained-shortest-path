#!/bin/bash


counter=1
while [ $counter -le 100 ]
do
    python -u "./dpath_generator.py"
    minizinc ../minizinc/bounded_dpath_implementation.mzn ./generatedTest.dzn 
    ((counter++))
done