f = open("results.txt","r")
tries = 202
lines = f.readlines()
for i in range(len(lines)/12):
    l=lines[i]
    