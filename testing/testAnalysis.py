import matplotlib.pyplot as plt 

f = open("results.txt","r")

dense=0
sparse=0

lines = f.readlines()
for test in range(200):
    nodes=int(lines[test*12][2:].split(";")[0])
    edges=int(lines[test*12][2:].split(";")[0])
    if (edges/(nodes*(nodes-1))>=0.5):
        dense+=1
    else:
        sparse+=1
    


print(f"Sparse: {sparse}")
print(f"Dense: {dense}")    

plt.bar(["Sparse", "Dense"], height=[sparse, dense], alpha=0.7)
plt.xlabel('Graph type')
plt.ylabel('Frequency')

plt.savefig('figure1.png')

plt.show()
