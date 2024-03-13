#!/bin/bash

echo "Hello!"

counter=1
ok=false
tries=0
while [ $counter -le 50 ]
do
    python -u "./dpath_generator.py"
    stTime=$(date +%s)
    output=$(timeout 15 minizinc --solver Gecode ../minizinc/bounded_dpath_implementation.mzn ./generatedTest.dzn)
    endTime=$(date +%s)
    error='ERROR'
    unsatisfiable='UNSATISFIABLE'
    ok=false
    if ! grep -qE "$error|$unsatisfiable" <<< "$output"; then
        cat ./generatedTest.dzn >> resultsTry.txt
        echo "" >> resultsTry.txt
        echo "$((endTime-stTime))" >> resultsTry.txt
        echo "Gecode" >> resultsTry.txt
        echo "$output" | head -n -2 | tail -n +3 >> resultsTry.txt
        ok=true
    else 
        echo "$output"
    fi 

    stTime=$(date +%s)
    output=$(timeout 15 minizinc --solver Chuffed ../minizinc/bounded_dpath_implementation.mzn ./generatedTest.dzn)
    endTime=$(date +%s)
    error='ERROR'
    unsatisfiable='UNSATISFIABLE'
    if ! grep -qE "$error|$unsatisfiable" <<< "$output"; then
        if [ "$ok" = false ]; then
            cat ./generatedTest.dzn >> resultsTry.txt
            echo "" >> resultsTry.txt
        fi
        echo "$((endTime-stTime))" >> resultsTry.txt
        echo "Chuffed" >> resultsTry.txt
        echo "$output" | head -n -3 | tail -n +3 >> resultsTry.txt
        ok=true
    else 
        echo "$output"
    fi

    if [ "$ok" = true ]; then
        ((counter++))
        echo "=========================================" >> resultsTry.txt
    fi
    ((tries++))
done
echo "Total tries = $tries" >> resultsTry.txt