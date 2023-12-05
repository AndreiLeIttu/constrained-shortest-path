import matplotlib.pyplot as plt 
from scipy.stats import linregress
import numpy as np

f = open("results.txt","r")

#585+24+508 tries

dense = 0
sparse = 0

nodeList = []
edgeList = []
timeList = []



lines = f.readlines()
for test in range(100):
    nodes = int(lines[test*13][2:].split(";")[0])
    edges = int(lines[test*13+1][2:].split(";")[0])
    t = int(lines[test*13+9].split('\n')[0])
    nodeList.append(nodes)
    edgeList.append(edges)
    timeList.append(t)


#Generating figure to see correlation between the number of edges and time
sumsDict = {}
countDict = {}

for key, value in zip(edgeList, timeList):
    if key in sumsDict:
        sumsDict[key]+=value
        countDict[key]+=1
    else:
        sumsDict[key]=value
        countDict[key] = 1
edgePoints=[key for key in sumsDict]
timeAvg=[int(sumsDict[key]/countDict[key]) for key in sumsDict]

slope, intercept, r_value, p_value, std_err = linregress(edgePoints, timeAvg)
line = slope * np.array(edgePoints) + intercept


plt.scatter(edgePoints, timeAvg, marker='o')
plt.plot(edgePoints, line)
plt.xlabel('Number of edges')
plt.ylabel('Avg runtime of the model in seconds')

plt.savefig("./figures/figure2.png")

plt.show()

#Generating figure to see correlation between the number of nodes and time
sumsDict = {}
countDict = {}

for key, value in zip(nodeList, timeList):
    if key in sumsDict:
        sumsDict[key]+=value
        countDict[key]+=1
    else:
        sumsDict[key]=value
        countDict[key] = 1
nodePoints=[key for key in sumsDict]
timeAvg=[int(sumsDict[key]/countDict[key]) for key in sumsDict]

slope, intercept, r_value, p_value, std_err = linregress(nodePoints, timeAvg)
line = slope * np.array(nodePoints) + intercept


plt.scatter(nodePoints, timeAvg, marker='o')
plt.plot(nodePoints, line)
plt.xlabel('Number of nodes')
plt.ylabel('Avg runtime of the model in seconds')

plt.savefig("./figures/figure3.png")

plt.show()

