import blobLinks
import sqlQuery
import mysql.connector
rawtablesqlstr="rawmanufact"

def getFields(line):
    fieldar=[-1,"manLab",0.000,-1,0,-1,0]
    commaloc=line.find(",")
    fieldindx=0
    while commaloc>=0:
        fieldstr=line[:commaloc]
        fieldar[fieldindx]=fieldstr
        fieldindx+=1
        commaloc+=1
        remstr=line[commaloc:]
        line=remstr
        commaloc=line.find(",")
    return fieldar

def readCSV(manID,manLab,timeF,rawID,rawQty,partID,partQty):
    manID.clear()
    timeF.clear()
    rawID.clear()
    partID.clear()
    partQty.clear()
    fin=open('RAWman.csv','r')
    line=fin.readline()
    while line:
        line=fin.readline()
        print(line)
        if(len(line)<2):
            break
        fieldsAr=getFields(line)
        for ii in range(len(fieldsAr)):
            print(fieldsAr[ii])
        manID.append(int(fieldsAr[0]))
        manLab.append(fieldsAr[1])
        timeFl=float(fieldsAr[2])
        if(timeFl<0.0):
            timeFl=0.0
        timeF.append(float(timeFl))
        rawID.append(int(fieldsAr[3]))
        rawQtyFl=float(fieldsAr[4])
        if rawQtyFl<0.0:
            rawQtyFl=0.0
        rawQty.append(rawQtyFl)
        partID.append(int(fieldsAr[5]))
        partQty.append(int(fieldsAr[6]))
    fin.close()

def writeLineToTable(conn,curs,mID, mLab,tiF,rID,rQty,IDar,Qtyar):
    if(len(IDar)<1):
        return False
    partIDBlob=blobLinks.linksToBlob(IDar)
    print(IDar)
    partQtyBlob=blobLinks.linksToBlob(Qtyar)
    print(Qtyar)
    rawLabel=sqlQuery.labelFromID(curs,rID)
    sqlcom="INSERT INTO "+rawtablesqlstr+" (MANID, MANLABEL, time, RAWID,RAWQTY,RAWLABEL,PARTID,PARTQTY) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    valar=(mID,mLab,tiF,rID,rQty,rawLabel,partIDBlob,partQtyBlob)
    print(sqlcom,valar)
    curs.execute(sqlcom,valar)
    conn.commit()
    return True

def writeToTable(conn,curs,manID,manLab,timeF,rawID,rawQty,partID,partQty):
    mlen=len(manID)
    if(mlen<1):
        return False
    lastManID=-1
    lastManLab=""
    lastTime=0.00
    lastRawID=-1
    lastRawQty=0
    manPartID=[]
    manPartQty=[]
    for i in range(mlen):
        print("current ID:", manID[i])
        if manID[i]!=lastManID or rawID[i]!=lastRawID:
            #print(lastManLab)
            #print(lastManID)
            #print(manPartID)
            #print(manPartQty,'\n')
            writeLineToTable(conn,curs,lastManID,lastManLab, lastTime,lastRawID,lastRawQty,manPartID,manPartQty)
            manPartID.clear()
            manPartQty.clear()
        lastManID=manID[i]
        lastManLab=manLab[i]
        lastTime=timeF[i]
        lastRawID=rawID[i]
        lastRawQty=rawQty[i]
        manPartID.append(partID[i])
        manPartQty.append(partQty[i])
    #print(lastManLab)
    #print(lastManID)
    #print(manPartID)
    #print(manPartQty,'\n')
    return writeLineToTable(conn,curs,lastManID,lastManLab,lastTime,lastRawID,lastRawQty, manPartID,manPartQty)

def createTable():
    conn = mysql.connector.connect(host="localhost",database="inventory",user="data0",password="pppp");
    curs=conn.cursor()
    manID=[]
    manLab=[]
    timeF=[]
    rawID=[]
    rawQty=[]
    partID=[]
    partQty=[]
    readCSV(manID,manLab,timeF,rawID,rawQty,partID,partQty)
    writeToTable(conn,curs,manID,manLab,timeF,rawID,rawQty,partID,partQty)
    conn.close()