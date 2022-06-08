from sre_constants import IN
import BOMtofields
import mysql.connector

def getID(curso):
    found_ID=-1
    numFound=0
    for row in curso:
        found_ID=row
        numFound+=1
    if numFound>1:
        found_ID=-1
    return found_ID

def matchID(curso, desc, intref):
    found_ID=-1
    if len(desc)<2:
        return found_ID
    if len(intref)>1:
        inqStr="SELECT U_ID FROM dummytest WHERE INTERNALREF =\'" + intref+"\'"
        curso.execute(inqStr)
        found_ID=getID(curso)
    if found_ID<0:
        inqStr="SELECT U_ID FROM dummytest WHERE LABEL LIKE \'%"+desc+"%\'"
        curso.execute(inqStr)
        found_ID=getID(curso)
    return found_ID

conn = mysql.connector.connect(host="localhost",database="parts_test2",user="data0",password="XXfish3x3")
curs=conn.cursor()

fin=open('odooBOMParts.csv','r')


dumpar=["NOF",-1, "NOF", -1, 0]
line = fin.readline()
cnt=0
BOMdesc=""
BOM_ID=-1
cnt_badBOM_match=0
cnt_badLAB_match=0
while line and cnt<10:
    line=fin.readline()
    fieldsAr=BOMtofields.getFields(line)
    if len(fieldsAr[1])>1:
        BOM_ID = matchID(curs, fieldsAr[1], fieldsAr[2])
        BOMdesc=fieldsAr[1]
        if(BOM_ID<0):
            cnt_badBOM_match+=1
    dumpar[0]=BOMdesc
    dumpar[1]=BOM_ID
    dumpar[2]=fieldsAr[4]
    dumpar[3]=matchID(curs, fieldsAr[4], fieldsAr[5])
    if(dumpar[3]<0):
        cnt_badLAB_match+=1
    dumpar[4]=fieldsAr[6]
    cnt+=1
print("bad BOM ID: ", cnt_badBOM_match)
print("bad Label ID: ", cnt_badLAB_match)
fin.close()
