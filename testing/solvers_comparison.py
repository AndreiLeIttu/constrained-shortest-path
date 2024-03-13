import matplotlib.pyplot as plt 
from scipy.stats import linregress
import numpy as np

#f = open("testfile.txt","r")
f = open("chuffed_gecode_results.txt","r")

#Total tries = 1466

lines = f.readlines()
chuffedLines = [index for index, string in enumerate(lines) if string == "Chuffed\n"]
successfulChuffed = len(chuffedLines)
gecodeLines = [index for index, string in enumerate(lines) if string == "Gecode\n"]
successfulGecode = len(gecodeLines)

print("Successful Gecode = " + str(successfulGecode) + " times")
print("Successful Chuffed = " + str(successfulChuffed) + " times")

onlyGecodeSuccess = 0
onlyChuffedSuccess = 0
bothSuccess = 0

for index in gecodeLines:
    if index+5 not in chuffedLines:
        onlyGecodeSuccess += 1
sumChuffed = 0
sumGecode = 0
chuffedFasterList = []
for index in chuffedLines:
    if index-5 in gecodeLines:
        timeChuffed = int(lines[index-1])
        timeGecode = int(lines[index-6])
        sumChuffed += timeChuffed
        sumGecode += timeGecode
        if timeChuffed<timeGecode:
            chuffedFasterList.append(index)
        bothSuccess += 1

    else:
        onlyChuffedSuccess += 1

totalSuccesses = onlyGecodeSuccess + onlyChuffedSuccess + bothSuccess
#percentage of only one solver success
onlyChuffedPercent = onlyChuffedSuccess * 100 / totalSuccesses
onlyGecodePercent = onlyGecodeSuccess * 100 / totalSuccesses
bothPercent = bothSuccess * 100 / totalSuccesses

print("Total time spent by chuffed on instances where both succeded: " + str(sumChuffed) + " seconds")
print("Total time spent by gecode on instances where both succeeded: " + str(sumGecode) + " seconds")
print("Gecode was overall " + str(round(sumGecode/sumChuffed*100,2)) + "% faster than Chuffed.")
print("Chuffed was faster " + str(len(chuffedFasterList)) + " times out of " + str(bothSuccess))

print("Percentage of tests where only Chuffed succeeded: " + str(onlyChuffedPercent) + "%")
print("Percentage of tests where only Gecode succeeded: " + str(onlyGecodePercent) + "%")
print("Percentage of tests where both solvers succeeded: " + str(bothPercent) + "%")

