import mysql.connector
import blobArray
import blobLinks

tablesqlstr="dummytest"

def qtyFromID(uID,curs):
    inqStr="SELECT QTY FROM "+tablesqlstr+" WHERE U_ID =\'" + str(uID)+"\'"
    curs.execute(inqStr)
    sqlout=curs.fetchone()[0]
    if not sqlout:
        return 0
    return sqlout

def labelFromID(uID,curs):
    inqStr="SELECT LABEL FROM "+tablesqlstr+" WHERE U_ID=\'"+str(uID)+"\'"
    curs.execute(inqStr)
    sqlout=curs.fetchone()[0]
    if not sqlout:
        return "UKN"
    return sqlout

def genSubReq(curs, uID, num, idUsed, numUsed, idReq, numReq):
    untrblob=blobLinks.getUntr(curs,uID,tablesqlstr)
    if not untrblob:
        return False
    untrNblob=blobLinks.getUntrN(curs,uID, tablesqlstr)
    if not untrNblob:
        return False
    linksar=blobArray.funcGetAr(untrblob)
    qtyar=blobArray.funcGetAr(untrNblob)
    if not len(linksar)==len(qtyar):
        return False
    arlen=len(linksar)
    if(arlen<=0):
        return False
    for i in range(arlen):
        numAvail=qtyFromID(linksar[i],curs)
        numRem=numAvail-(num * qtyar[i])
        curNumUsed=(num * qtyar[i])
        if(numRem<0):
            idReq.append(linksar[i])
            numReq.append(-numRem)
            if(numAvail>0):
                curNumUsed=numAvail
        if(curNumUsed>0):
            idUsed.append(linksar[i])
            numUsed.append(curNumUsed)
    return True


def getConsumed(curs, uID, numKit, feedLev, feedID, feedNum, consumeLev, consumeID, consumeNum):
    idUsed=[]
    numUsed=[]
    idReq=[]
    numReq=[]

    ar_i=0
    feedLev.append(0)
    feedID.append(uID)
    feedNum.append(numKit)
    feed_i=1
    consume_i=0

    lev=0
    goOn=True
    while goOn:
        lev=feedLev[ar_i]
        curUID=feedID[ar_i]
        curNum=feedNum[ar_i]
        goDown=genSubReq(curs, curUID, curNum, idUsed, numUsed,idReq,numReq)
        if goDown:
            for i_con in range(len(idUsed)):
                consumeID.append(idUsed[i_con])
                consumeNum.append(numUsed[i_con])
                consumeLev.append(lev+1)
                consume_i+=1
            for i_req in range(len(idReq)):
                feedID.appened(idReq[i_req])
                feedNum.append(numReq[i_req])
                feedLev.append(lev+1)
                feed_i+=1
        ar_i+=1
        goOn=ar_i<feed_i

    return lev

def writeLineReq(conn, curs, orderRef, kitUID, lev, uID, numReq):
    partLabel=labelFromID(curs,uID)
    outStr="         UID: "+str(uID)+" | "+partLabel+"  | not in inv: "+numReq

def genKitReq(conn, curs, orderRef, uID, numKit):
    workLev=[]
    workID=[]
    workNum=[]
    usedLev=[]
    usedID=[]
    usedNum=[]
    getConsumed(curs,uID,numKit,workLev,workID,workNum,usedLev,usedID,usedNum)
    lenUsed=len(usedID)
    lenWork=len(workID)
    maxLevWork=workLev[lenWork-1]
    maxLevUsed=usedLev[lenUsed-1]
    
    kitLabel=labelFromID(curs,uID)
    print("---------------------------------\n\n")
    #headerStr="Order, Kit,  lev, subID, Number Used, Number Ass"
    headerStr="Order: "+orderRef+"  Kit ID: "+str(uID)+" | "+kitLabel
    print(headerStr)
    lastLev=0
    for i in range(lenWork):
        if(workLev[i]!=lastLev):
            print("--------")
            print("   :", workLev[i])
            lastLev=workLev[i]
        writeLineReq(conn,curs,orderRef,uID,workLev[i],workID[i],workNum[i])
    print("---------------------------------\n\n")

    

conn = mysql.connector.connect(host="localhost",database="parts_test2",user="data0",password="XXfish3x3");
tablesqlstr="dummytest"

curs=conn.cursor();



conn.close()
