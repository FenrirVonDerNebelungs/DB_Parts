import parseDesc
import refMatch
import mysql.connector

conn = mysql.connector.connect(host="localhost",database="inventory",user="data0",password="pppp");
tablesqlstr="units"
curs=conn.cursor();

fieldsar = ["dum1", "desc", "IRef", "dum2", "SaleP", "Cost", "QTY", "dum3", "dum4"]
fin=open('Product Template (product.template).csv','r')
line = fin.readline()
cnt=0
cnt_nof=0
cnt_updt=0
while line and cnt<1000:
    line=fin.readline()
    line=parseDesc.funcFix(line)
    line=parseDesc.funcFix(line)
    #print(line)
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
    if fieldindx<=0:
        print("end of file")
        break
    vallable=fieldsar[1]
    valintref=parseDesc.funcRemQuotes(fieldsar[2])
    valqty=parseDesc.funcRemQuotes(fieldsar[6])
    uIDmatched=refMatch.matchID(curs,tablesqlstr,vallable,valintref)
    if uIDmatched>=0:
        inqStr="UPDATE "+tablesqlstr+" SET ODQTY="+str(valqty)+" WHERE U_ID="+str(uIDmatched)
        curs.execute(inqStr)
        conn.commit()
        cnt_updt+=1
        ptrstr=" | "+vallable+" | "+valintref+" | "+str(uIDmatched)+" | "+str(valqty)
        print(ptrstr)
    else:
        cnt_nof+=1
        print("Not Found: ",vallable)
    cnt+=1
print("total records: ", cnt)
print(" num updated: ",cnt_updt)
print("   not found: ",cnt_nof)
ynin=input("update QTY to Odoo qty? y/n:")
if ynin=='y':
    inqStr="UPDATE "+tablesqlstr+" SET QTY=ODQTY"
    curs.execute(inqStr)
    conn.commit()
fin.close()
conn.close()