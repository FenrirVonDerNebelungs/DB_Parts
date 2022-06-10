import mysql.connector
import blobLinks

def getBlob(curso):
    blob = curso.fetchone()[0]
    return blob

def sendToDB(sqlconn, curso, bomid, links_ar):
    if(len(links_ar)<2):
        return False
    unterblob=blobLinks.linksToBlob(bomid,links_ar)
    sqlcom="INSERT INTO units (UNTR) VALUES (%s)"
    curso.execute(sqlcom, unterblob)
    sqlconn.commit()
    for i in range(len(links_ar)):
        inqStr="SELECT UBER FROM units WHERE U_ID=\'"+str(links_ar[i])+"\'"
        uberblob=getblob(curso)
        if(blobLinks.addUberLink(uberblob)):
            sqlcom="INSERT INTO units (UBER) VALUES (%s)"
            curso.execute(sqlcom,uberblob)
            sqlconn.commit()

conn = mysql.connector.connect(host="localhost",database="parts_test2",user="data0",password="XXfish3x3")
curs=conn.cursor()

fin=open('BOMmatched.csv','r')
inar=["NOF",-1,"NOF",-1,0]

cnt=0
line=fin.readline()
BOMID=-1
linksUIDs=[]
while line and cnt<10:
    commaloc=line.find(",")
    fieldindx=0
    while commaloc>=0:
        fieldstr=line[:commaloc]
        fieldindx+=1
        commaloc+=1
        line=line[commaloc:]
        commaloc=line.find(",")
    #process these fields if enough good fields found
    if(fieldindx<4):
        break
    (bom_uid,)=fieldstr[1]
    if(bom_uid!=BOMID):
        sendToDB(conn,curs,BOMID,linksUIDs)
        linksUIDs.clear()
        BOMID=bom_uid
    (link_uid,)=fieldstr[3]
    linksUIDs.append(link_uid)
    #finish lines loop
    cnt+=1
    line=fin.readline()
    if not line:
        sendToDB(curs,BOMID,linksUIDs)

fin.close()
conn.close()