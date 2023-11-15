import numpy as np
import random

nodes = random.randint(1,100)
edges = random.randint(1,min((nodes-1)*nodes/2,100))
source = random.randint(1,nodes)
target = random.randint(1,nodes)
while(target==source):
    target = random.randint(1,nodes)

#constraint sets generation
numConstraintSets = random.randint(0,10)
constraintSets = []
constrString = "["

for i in range(numConstraintSets):
    constrString+="{"
    size = random.randint(1,10)
    print(size)
    arr = np.random.randint(1,nodes,size)
    constraintSets.append(arr)
    for num in range(len(arr)-1):
        constrString+=str(arr[num])+','
    constrString+=str(arr[len(arr)-1])
    constrString+="},"
if  numConstraintSets!=0:
    constrString=constrString[:-1]
constrString += "]"

#edges generation
toNodes = []
fromNodes = []
weights = []

for i in range(edges):
    weight = random.randint(0,100)
    x = random.randint(1,nodes)
    y = random.randint(1,nodes)
    while (x==y):
        y=random.randint(1,nodes)
    toNodes.append(x)
    fromNodes.append(y)
    weights.append(weight)

#printing to another file 
f = open("./generatedTest.dzn", "w")
output = ""
output += f"N={nodes};\nE={edges};\nC={numConstraintSets};\nsource={source};\ntarget={target};\nfrom={fromNodes};\nto={toNodes};\nweights={weights};\nv_constraint="+constrString
f.write(output)

