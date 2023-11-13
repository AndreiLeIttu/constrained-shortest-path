import numpy as np
import random

nodes = random.randint(1,100)
edges = random.randint(1,1000)
source = random.randint(1,nodes)
target = random.randint(1,nodes)
while(target==source):
    target = random.randint(1,nodes)

#constraint sets generation
numConstraintSets = random.randint(0,10)
constraintSets=[]
for i in numConstraintSets:
    size = random.randint(1,10)
    arr = np.randint(1,nodes,size)
    constraintSets.append(arr)





