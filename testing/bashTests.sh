#!/bin/bash

echo "Hello!"

counter=1
tries=0
while [ $counter -le 50 ]
do
    python -u "./dpath_generator.py"
    stTime=$(date +%s)
    output=$(timeout 15 minizinc ../minizinc/bounded_dpath_implementation.mzn ./generatedTest.dzn)
    endTime=$(date +%s)
    error='ERROR'
    unsatisfiable='UNSATISFIABLE'
    if ! grep -qE "$error|$unsatisfiable" <<< "$output"; then
        cat ./generatedTest.dzn >> results.txt
        echo "" >> results.txt
        echo "$((endTime-stTime))" >> results.txt
        echo "$output" | head -n -2 | tail -n +3 >> results.txt
        ((counter++))
    else 
        echo "$output"
    fi
    ((tries++))
done
echo "$tries"