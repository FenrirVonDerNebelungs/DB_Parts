
fin=open('OdooAllParts00.csv','r')

#flines=fin.readlines()

line = fin.readline()
cnt=0
while line:
    line=fin.readline()
    print(line)

fin.close()