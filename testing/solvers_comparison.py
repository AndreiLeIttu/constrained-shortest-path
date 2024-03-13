import matplotlib.pyplot as plt 
from scipy.stats import linregress
import numpy as np

f = open("testfile.txt","r")

lines = f.readlines()
chuffedLines = [index for index, string in enumerate(lines) if string == "Chuffed\n"]
successfulChuffed = len(chuffedLines)
gecodeLines = [index for index, string in enumerate(lines) if string == "Gecode\n"]
successfulGecode = len(gecodeLines)

print("Successful Gecode = " + str(successfulGecode))
print("Successful Chuffed = " + str(successfulChuffed))


