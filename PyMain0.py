import mysql.connector

conn = mysql.connector.connect(host="localhost",database="parts_test2",user="data0",password="XXfish3x3");

curs=conn.cursor();
curs.execute("SHOW DATABASES")
for db in curs:
    print(db)

sqlcom = "INSERT INTO units (TYPE, LABEL, QTY, INTERNALREF, COST, SALESPRICE) VALUES (%s, %s, %s, %s, %s, %s)"

fin=open('OdooAllParts00.csv','r')

fieldsar = ["dum1", "desc", "IRef", "dum2", "SaleP", "Cost", "QTY", "dum3", "dum4"]
line = fin.readline()
cnt=0
while line and cnt<1000:
    line=fin.readline()
    print(line)
    commaloc=line.find(",")
    fieldindx=0
    while commaloc>=0:
        fieldstr=line[:commaloc]
        fieldsar[fieldindx]=fieldstr
        fieldindx+=1
        commaloc+=1
        remstr=line[commaloc:]
        line=remstr
        commaloc=line.find(",")
    cnt+=1
    if fieldindx<=0:
        print("end")
        break
    valtype='PART'
    vallable=fieldsar[1]
    valqty = fieldsar[6]
    valintref=fieldsar[2]
    valcost=fieldsar[5]
    valsale=fieldsar[4]
    valar=(valtype, vallable, valqty, valintref, valcost, valsale)
    curs.execute(sqlcom,valar)
    conn.commit()
    print(curs.rowcount, "record inserted")

fin.close()





