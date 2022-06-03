import parseDesc
fin=open('odooBOMParts.csv','r')

fieldsar = ["bomdesc", "desc", 0]
line = fin.readline()
cnt=0
BOMdesc=""
while line and cnt<10:
    line=fin.readline()
    print(line)
    fixed00=parseDesc.funcFix(line)
    print(fixed00)
    fixed0=parseDesc.funcFix(fixed00)
    print(fixed0)
    fixed=parseDesc.funcFix(fixed0)
    print(fixed)
    commaloc=fixed.find(",")
    fieldindx=0
    while commaloc>=0:
        fieldstr=fixed[:commaloc]
        fieldsar[fieldindx]=fieldstr
        #print(fieldsar[fieldindx])
        #print(len(fieldsar[fieldindx]))
        #print(fieldindx)
        fieldindx+=1
        commaloc+=1
        remstr=fixed[commaloc:]
        fixed=remstr
        commaloc=fixed.find(",")
    cnt+=1

fin.close()
