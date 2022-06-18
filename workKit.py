import mysql.connector
import blobArray
import blobLinks

tablesqlstr="dummytest"

def qtyFromID(curs,uID):
    inqStr="SELECT QTY FROM "+tablesqlstr+" WHERE U_ID =\'" + str(uID)+"\'"
    curs.execute(inqStr)
    sqlout=curs.fetchone()[0]
    if not sqlout:
        return 0
    return sqlout

def labelFromID(curs,uID):
    inqStr="SELECT LABEL FROM "+tablesqlstr+" WHERE U_ID=\'"+str(uID)+"\'"
    curs.execute(inqStr)
    sqlout=curs.fetchone()[0]
    if not sqlout:
        return "UKN"
    return sqlout

def locFromID(curs, uID):
    inqStr="SELECT LOC FROM "+tablesqlstr+" WHERE U_ID=\'"+str(uID)+"\'"
    curs.execute(inqStr)
    sqlout=curs.fetchone()[0]
    if not sqlout:
        return "UN"
    return sqlout

def locShelfFromID(curs, uID):
    inqStr="SELECT LOC_SHELF FROM "+tablesqlstr+" WHERE U_ID=\'"+str(uID)+"\'"
    curs.execute(inqStr)
    sqlout=curs.fetchone()[0]
    if not sqlout:
        return "UN"
    return sqlout

def getAssIDQty(curs, uID):
    untrblob=blobLinks.getUntr(curs,uID,tablesqlstr)
    if not untrblob:
        return [],[]
    untrNblob=blobLinks.getUntrN(curs,uID, tablesqlstr)
    if not untrNblob:
        return [],[]
    IDar=blobArray.funcGetAr(untrblob)
    QTYar=blobArray.funcGetAr(untrNblob)
    if not len(IDar)==len(QTYar):
        return [],[]
    return IDar,QTYar

def printAss(curs, uID):
    IDar, QTYar=getAssIDQty(curs, uID)
    topLab=labelFromID(curs,uID)
    tpStr="Assembly:  "+str(uID)+"  | "+topLab
    print(tpStr)
    for i in range(len(IDar)):
        subLab=labelFromID(curs,IDar[i])
        prStr="    | "+str(IDar[i])+" | "+subLab+"  | "+str(QTYar[i])
        print(prStr)



def genSubReq(curs, uID, num, idUsed, numUsed, idReq, numReq):
    linksar, qtyar=getAssIDQty(curs,uID)
    arlen=len(linksar)
    if(arlen<=0):
        return False
    for i in range(arlen):
        numAvail=qtyFromID(curs,linksar[i])
        if numAvail<0:
            numAvail=0
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

def mergeDup(aLev,aID,aNum):
    alen=len(aLev)
    for i in range(alen):
        curID=aID[i]
        for j in range(i+1,alen):
            nextID=aID[j]
            if(curID==nextID):
                aNum[i]=aNum[i]+aNum[j]
                aLev[j]=-1
    oLev=[]
    oID=[]
    oNum=[]
    for i in range(alen):
        oLev.append(aLev[i])
        oID.append(aID[i])
        oNum.append(aNum[i])
    aLev.clear()
    aID.clear()
    aNum.clear()
    for i in range(len(oLev)):
        if oLev[i]>=0:
            aLev.append(oLev[i])
            aID.append(oID[i])
            aNum.append(oNum[i])

def getAll(curs,uID,num,feedLev,feedID, feedNum, hasDown):
    feedLev.clear()
    feedID.clear()
    feedNum.clear()
    hasDown.clear()

    ar_i=0
    lev=0
    feedLev.append(0)
    feedID.append(uID)
    feedNum.append(num)
    hasDown.append(False)
    feed_i=1
    goOn=True
    while goOn:
        lev=feedLev[ar_i]
        curUID=feedID[ar_i]
        curNum=feedNum[ar_i]
        linksar,qtyar=getAssIDQty(curs,curUID)
        lenLinks=len(linksar)
        if(lenLinks>0):
            hasDown[ar_i]=True
        for i in range(lenLinks):
            feedLev.append(lev+1)
            feedID.append(linksar[i])
            feedNum.append(qtyar[i]*curNum)
            hasDown.append(False)
            feed_i+=1
        ar_i+=1
        goOn=ar_i<feed_i
    return lev

def getRaw(curs, uID, num, levUsed, idUsed, numUsed):
    levUsed.clear()
    idUsed.clear()
    numUsed.clear()
    feedLev=[]
    feedID=[]
    feedNum=[]
    hasDown=[]
    getAll(curs,uID,num,feedLev, feedID, feedNum,hasDown)
    for i in range(len(feedID)):
        if not hasDown[i]:
            levUsed.append(feedLev[i])
            idUsed.append(feedID[i])
            numUsed.append(feedNum[i])

def getConsumed(curs, uID, numKit, feedLev, feedID, feedNum, consumeLev, consumeID, consumeNum):
    idUsed=[]
    numUsed=[]
    idReq=[]
    numReq=[]

    feedLev.clear()
    feedID.clear()
    feedNum.clear()
    consumeLev.clear()
    consumeID.clear()
    consumeNum.clear()

    ar_i=0
    feedLev.append(0)
    feedID.append(uID)
    feedNum.append(numKit)
    feed_i=1
    consume_i=0

    lev=0
    goOn=True
    cnt=0
    while goOn and cnt<1000:
        lev=feedLev[ar_i]
        curUID=feedID[ar_i]
        curNum=feedNum[ar_i]
        print("curUID: ", curUID)
        print("curNUm: ", curNum)
        print(" ar_i: ", ar_i)
        print(" feed_i: ", feed_i)
        idUsed.clear()
        numUsed.clear()
        idReq.clear()
        numReq.clear()
        goDown=genSubReq(curs, curUID, curNum, idUsed, numUsed,idReq,numReq)
        if goDown:
            for i_con in range(len(idUsed)):
                consumeID.append(idUsed[i_con])
                consumeNum.append(numUsed[i_con])
                consumeLev.append(lev+1)
                consume_i+=1
            for i_req in range(len(idReq)):
                print("ID Req: ", idReq)
                feedID.append(idReq[i_req])
                feedNum.append(numReq[i_req])
                feedLev.append(lev+1)
                feed_i+=1
        print("consumed: ",consumeID)
        print("feed: ",feedID)
        ar_i+=1
        goOn=ar_i<feed_i
        cnt+=1
    return lev

def findUsedMatchedToReq(workID, usedID, usedNum):
    nUsed=[]
    for i in range(len(workID)):
        uid=workID[i]
        if uid in usedID:
            j = usedID.index(uid)
            nUsed.append(usedNum[j])
        else:
            nUsed.append(0)
    return nUsed

def writeLineRaw(conn,curs,orderRef,kitUID,lev,uID,numAvail,numReq):
    uidStr=str(uID)
    numAvailStr=str(numAvail)
    numStr=str(numReq)
    partLabel=labelFromID(curs,uID)
    loc=locFromID(curs,uID)
    locshelf=locShelfFromID(curs,uID)
    locStr=loc+locshelf
    InvFlag=""
    if(numAvail<numReq):
        InvFlag="*"
    #print(f"    UID: {uidStr:8} | {partLabel:50} | Avail: {numAvailStr:8} | Used: {numStr:8}{InvFlag:1}")
    print(f"{uidStr:8}, {partLabel:50}, {locStr:4}, {numAvailStr:8}, {numStr:8}, {InvFlag:1}")

def writeLineReq(conn, curs, orderRef, kitUID, lev, uID, numUsed, numReq):
    partLabel=labelFromID(curs,uID)
    outStr="         UID: "+str(uID)+" | "+partLabel+"   | used: "+str(numUsed)+"  | not in inv: "+str(numReq)
    print(outStr)

def genKitRaw(conn,curs,orderRef,uID,numKit):
    usedLev=[]
    usedID=[]
    usedNum=[]
    getRaw(curs, uID, numKit, usedLev, usedID, usedNum)
    mergeDup(usedLev,usedID,usedNum)
    kitLabel=labelFromID(curs,uID)
    print("---------------------------------\n\n")
    headerStr="Order: "+orderRef+"  Kit ID: "+str(uID)+" | "+kitLabel+" | "+str(numKit)
    print(headerStr)
    lastLev=0
    for i in range(1,len(usedID)):
        if(usedLev[i]!=lastLev):
            print("--------")
            print("   :", usedLev[i])
            lastLev=usedLev[i]
        AvailQty=qtyFromID(curs,usedID[i])
        writeLineRaw(conn,curs,orderRef,uID,usedLev[i],usedID[i],AvailQty,usedNum[i])
    print("---------------------------------\n\n")

def genKitReq(conn, curs, orderRef, uID, numKit):
    workLev=[]
    workID=[]
    workNum=[]
    usedLev=[]
    usedID=[]
    usedNum=[]
    getConsumed(curs,uID,numKit,workLev,workID,workNum,usedLev,usedID,usedNum)
    mergeDup(workLev,workID,workNum)#takes out duplicate IDs and adds them instead for only one instance
    mergeDup(usedLev,usedID,usedNum)
    usedForReqNum=findUsedMatchedToReq(workID,usedID,usedNum)
    lenUsed=len(usedID)
    lenWork=len(workID)
    maxLevWork=workLev[lenWork-1]
    maxLevUsed=usedLev[lenUsed-1]
    
    kitLabel=labelFromID(curs,uID)
    print("---------------------------------\n\n")
    #headerStr="Order, Kit,  lev, subID, Number Used, Number Ass"
    headerStr="Order: "+orderRef+"  Kit ID: "+str(uID)+" | "+kitLabel + " | "+str(numKit)
    print(headerStr)
    lastLev=0
    for i in range(1,lenWork):
        if(workLev[i]!=lastLev):
            print("--------")
            print("   :", workLev[i])
            lastLev=workLev[i]
        writeLineReq(conn,curs,orderRef,uID,workLev[i],workID[i],usedForReqNum[i],workNum[i])
    print("---------------------------------\n\n")


def runK(uID,numKit):    
    conn = mysql.connector.connect(host="localhost",database="parts_test2",user="data0",password="XXfish3x3");
    curs=conn.cursor();
    genKitReq(conn,curs,"S0000",uID,numKit)
    genKitRaw(conn,curs,"S0000",uID,numKit)
    conn.close()
