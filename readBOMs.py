import BOMtofields
import refMatch
import mysql.connector

tablesqlstr="units"

conn = mysql.connector.connect(host="localhost",database="inventory",user="data0",password="pppp");
curs=conn.cursor()

fin=open('odooBOMParts.csv','r')
fout=open('BOMmatched.csv', 'w')

dumpar=["NOF",-1, "NOF", -1, 0]
line = fin.readline()
cnt=0
BOMdesc=""
BOM_ID=-1
cnt_totBOMs=0
cnt_badBOM_match=0
cnt_badLAB_match=0
while line and cnt<1000:
    line=fin.readline()
    if(len(line)<2):
        break
    #print(line)
    fieldsAr=BOMtofields.getFields(line)
    if len(fieldsAr[1])>1:
        cnt_totBOMs+=1
        BOM_ID = refMatch.matchID(curs, tablesqlstr, fieldsAr[1], fieldsAr[2])
        BOMdesc=fieldsAr[1]
        if(BOM_ID<0):
            cnt_badBOM_match+=1
    dumpar[0]=BOMdesc
    dumpar[1]=BOM_ID
    dumpar[2]=fieldsAr[4]
    dumpar[3]=refMatch.matchID(curs, tablesqlstr, fieldsAr[4], fieldsAr[5])
    if(dumpar[3]<0):
        cnt_badLAB_match+=1
    dumpar[4]=fieldsAr[6]
    dumpStr=""
    for str_i in range(5):
        dumpStr+=str(dumpar[str_i])+","
    dumpStr+=str(cnt)+',\n'
    print(dumpStr)
    fout.write(dumpStr)
    cnt+=1
print("total BOMs: ", cnt_totBOMs)
print("bad BOM ID: ", cnt_badBOM_match)
print("bad Label ID: ", cnt_badLAB_match)
fout.close()
fin.close()
conn.close()
