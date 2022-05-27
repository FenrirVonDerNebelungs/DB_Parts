
fin=open('OdooAllParts00.csv','r')

#flines=fin.readlines()
fieldsar = ["dum1", "desc", "IRef", "dum2", "SaleP", "Cost", "QTY", "dum3", "dum4"]
line = fin.readline()
cnt=0
while line and cnt<2:
    line=fin.readline()
    print(line)
    commaloc=line.find(",")
    fieldindx=0
    while commaloc>=0:
        fieldstr=line[:commaloc]
        fieldsar[fieldindx]=fieldstr
        print(fieldsar[fieldindx])
        print(fieldindx)
        fieldindx+=1
        commaloc+=1
        remstr=line[commaloc:]
        line=remstr
        commaloc=line.find(",")
    cnt+=1

fin.close()