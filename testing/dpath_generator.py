import numpy as np
import random
from queue import Queue

nodes = random.randint(101,1000)
edges = random.randint(101,1000)
#source = random.randint(1,nodes)
#target = random.randint(1,nodes)
#while(target==source):
#    target = random.randint(1,nodes)

#constraint sets generation
numConstraintSets = random.randint(0,10)
constraintSets = []
constrString = "["

for i in range(numConstraintSets):
    constrString+="{"
    size = random.randint(1,100)
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

v=[]
for i in range(0,nodes+1):
    v.append([])

for i in range(edges):
    weight = random.randint(0,1000)
    x = random.randint(1,nodes)
    if i==0:
        source=x
    y = random.randint(1,nodes)
    while (x==y):
        y=random.randint(1,nodes)
    toNodes.append(x)
    fromNodes.append(y)
    weights.append(weight)
    v[x].append(y)

#searching for two nodes with a road between them
target=10

connected=[]
connected.append(source)

q = Queue()
q.put(source)
while not q.empty():
    top=q.get()
    for vec in v[top]:
        if vec not in connected:
            connected.append(vec)
            q.put(vec)
if len(connected)!=1:
    target = random.choice(connected[1:])
print(source)

#printing to another file 
f = open("./generatedTest.dzn", "w")
output = ""
output += f"N={nodes};\nE={edges};\nC={numConstraintSets};\nsource={source};\ntarget={target};\nfrom={fromNodes};\nto={toNodes};\nweights={weights};\nv_constraint="+constrString
f.write(output)

