import mysql.connector
import blobLinks

tablesqlstr="dummytest"

#def getBlob(curso):
#    blob = curso.fetchone()[0]
#    return blob

def sendToDB(sqlconn, curso, bomid, links_ar, num_ar):
    if(len(links_ar)<2):
        return False
    unterblob=blobLinks.linksToBlob(links_ar)
    sqlcom="UPDATE "+tablesqlstr+" SET UNTR=%s WHERE U_ID=%s"
    inargs=(unterblob,bomid)
    curso.execute(sqlcom,inargs)
    unterNblob=blobLinks.linksToBlob(num_ar)
    sqlcom1="UPDATE "+tablesqlstr+" SET UNTRN=%s WHERE U_ID=%s"
    inargs1=(unterNblob,bomid)
    curso.execute(sqlcom1,inargs1)
    sqlcom2="UPDATE "+tablesqlstr+" SET TYPE=%s WHERE U_ID=%s"
    inargs2=('ASS',bomid)
    curso.execute(sqlcom2, inargs2)
    sqlconn.commit()
    for i in range(len(links_ar)):
#        inqStr="SELECT UBER FROM "+tablesqlstr+" WHERE U_ID=\'"+str(links_ar[i])+"\'"
#        curso.execute(inqStr)
#        uberblob=getBlob(curso)
        uberblob=blobLinks.getUber(curso,links_ar[i],tablesqlstr)
        if not uberblob:
            uberblob=blobLinks.newBlob()
        if(blobLinks.addUberLink(links_ar[i],uberblob)):
            sqlcom="UPDATE "+tablesqlstr+" SET UBER=%s WHERE U_ID=%s"
            inargs=(uberblob,links_ar[i])
            curso.execute(sqlcom,inargs)
            sqlconn.commit()
    return True

conn = mysql.connector.connect(host="localhost",database="parts_test2",user="data0",password="XXfish3x3")
curs=conn.cursor()

fin=open('BOMmatched.csv','r')
fieldstr=["NOF",-1,"NOF",-1,0]

cnt=0
line=fin.readline()
BOMID=-1
linksUIDs=[]
linksQTYs=[]
while line and cnt<1000:
    commaloc=line.find(",")
    fieldindx=0
    while commaloc>=0:
        fieldstr[fieldindx]=line[:commaloc]
        fieldindx+=1
        commaloc+=1
        line=line[commaloc:]
        commaloc=line.find(",")
    #process these fields if enough good fields found
    if(fieldindx<4):
        break
    print(fieldstr[0], fieldstr[1], fieldstr[2], fieldstr[3], fieldstr[4], sep=", ")
    bom_uid=int(fieldstr[1])
    if(bom_uid!=BOMID):
        print("sending bomID", BOMID)
        print("links: ", linksUIDs)
        print("QTYs:  ", linksQTYs)
        print('-------')
        sendToDB(conn,curs,BOMID,linksUIDs,linksQTYs)
        linksUIDs.clear()
        linksQTYs.clear()
        BOMID=bom_uid
    link_uid=int(fieldstr[3])
    linksUIDs.append(link_uid)
    link_qty=int(fieldstr[4])
    linksQTYs.append(link_qty)
    #finish lines loop
    cnt+=1
    line=fin.readline()
    if not line:
        print("sending bomID", BOMID)
        print("links: ", linksUIDs)
        print("QTYs:  ", linksQTYs)
        sendToDB(conn,curs,BOMID,linksUIDs,linksQTYs)

fin.close()
conn.close()