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

def typeFromID(curs,uID):
    inqStr="SELECT TYPE FROM "+tablesqlstr+" WHERE U_ID=\'"+str(uID)+"\'"
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

def getAssIDQty(curs, uID):
    return blobLinks.getLinksQTYs(curs,tablesqlstr,uID)

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
    partype=typeFromID(uID)
    if partype.find('MAN')>=0 or partype=='RAW':
        return False
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

def genReqArrays(curs, uID, num, ids, numUsed, numReq):
    partype=typeFromID(uID)
    if partype.find('MAN')>=0 or partype=='RAW':
        return False
    linksar,qtyar=getAssIDQty(curs,uID)
    arlen=len(linksar)
    if(arlen<=0):
        return False
    for i in range(arlen):
        numTarget=num*qtyar[i]
        numAvail=qtyFromID(curs,linksar[i])
        if(numAvail<0):
            numAvail=0
        numRem=numAvail-numTarget
        curNumUsed=numTarget
        numMissing=0
        if numRem<0:
            curNumUsed=numAvail
            numMissing=(-numRem)
        ids[i]=linksar[i]
        numUsed[i]=curNumUsed
        numReq[i]=numMissing
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

def mergeDupAll(aLev,aPar,aID,aNum,aUsed,aReq, aDown):
    alen=len(aLev)
    for i in range(alen):
        curID=aID[i]
        for j in range(i+1,alen):
            nextID=aID[j]
            if(curID==nextID):
                aUsed[i]=aUsed[i]+aUsed[j]
                aReq[i]=aReq[i]+aReq[j]
                if(aLev[j]<aLev[i]):
                    aLev[i]=aLev[j]
                    aPar[i]=aPar[j]
                aLev[j]=-1
    oLev=[]
    oPar=[]
    oID=[]
    oNum=[]
    oUsed=[]
    oReq=[]
    oDown=[]
    for i in range(alen):
        oLev.append(aLev[i])
        oPar.append(aPar[i])
        oID.append(aID[i])
        oNum.append(aNum[i])
        oUsed.append(aUsed[i])
        oReq.append(aReq[i])
        oDown.append(aDown[i])
    aLev.clear()
    aPar.clear()
    aID.clear()
    aNum.clear()
    aUsed.clear()
    aReq.clear()
    aDown.clear()
    for i in range(len(oLev)):
        if oLev[i]>=0:
            aLev.append(oLev[i])
            aPar.append(oPar[i])
            aID.append(oID[i])
            aNum.append(oNum[i])
            aUsed.append(oUsed[i])
            aReq.append(oReq[i])
            aDown.append(oDown[i])

def getAll(curs,uID,num,feedLev,feedParent,feedID, feedNum, feedUsed, feedReq, hasDown):
    feedLev.clear()
    feedParent.clear()
    feedID.clear()
    feedNum.clear()
    feedUsed.clear()
    feedReq.clear()
    hasDown.clear()

    ar_i=0
    lev=0
    feedLev.append(0)
    feedParent.append(uID)
    feedID.append(uID)
    feedNum.append(num)
    hasDown.append(False)
    feed_i=1
    goOn=True
    while goOn:
        lev=feedLev[ar_i]
        curUID=feedID[ar_i]
        linksar=[]
        numUsed=[]
        numReq=[]
        gotArrays=genReqArrays(curs,uID,num,linksar,numUsed,numReq)
        lenLinks=0
        if(gotArrays):
            hasDown[ar_i]=True
            lenLinks=len(linksar)
        for i in range(lenLinks):
            qty=qtyFromID(linksar[i])
            feedLev.append(lev+1)
            feedParent.append(curUID)
            feedID.append(linksar[i])
            feedNum.append(qty)
            feedUsed.append(numUsed[i])
            feedReq.append(numReq[i])
            hasDown.append(False)
            feed_i+=1
        ar_i+=1
        goOn=ar_i<feed_i
    return lev


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

def writeLineAllcsv(curs, parentID, uID, numAvail, numUsed, numReq):
    parentIDstr=""
    if parentID>=0:
        parentIDstr=str(parentID)
    uidStr=str(uID)
    numAvailStr=str(numAvail)
    numUsedStr=str(numUsed)
    numReqStr=str(numReq)
    parentLabel=""
    if parentID>=0:
        parentLabel=labelFromID(curs,uID)
    partLabel=labelFromID(curs,uID)
    loc=locFromID(curs,uID)
    locshelf=locShelfFromID(curs,uID)
    locStr=loc+locshelf
    InvFlag=""
    if(numAvail<numReq):
        InvFlag="INV!"
    print(f"{parentIDstr:8}, {parentLabel:200}, {uidStr:8}, {partLabel:50}, {locStr:4}, {numAvailStr:8}, {numUsedStr:8}, {numReqStr:8},{InvFlag:4}")


def writeLineReq(conn, curs, orderRef, kitUID, lev, uID, numUsed, numReq):
    partLabel=labelFromID(curs,uID)
    outStr="         UID: "+str(uID)+" | "+partLabel+"   | used: "+str(numUsed)+"  | not in inv: "+str(numReq)
    print(outStr)

def genKitAll(conn,curs,orderRef,uID,numKit):
    usedLev=[]
    usedParent=[]
    usedID=[]
    availNum=[]
    usedNum=[]
    reqNum=[]
    hasDown=[]
    getAll(curs,uID,numKit,usedLev,usedParent,usedID,availNum,usedNum,reqNum,hasDown)
    lastParent=-1
    for i in range(len(usedID)):
        parentID=-1
        if(usedParent[i]!=lastParent):
            parentID=usedParent[i]
            lastParent=parentID
        writeLineAllcsv(curs,parentID,usedID[i],availNum[i],usedNum[i],reqNum[i])

def genKitReq(conn,curs,orderRef,uID,numKit):
    usedLev=[]
    usedParent=[]
    usedID=[]
    availNum=[]
    usedNum=[]
    reqNum=[]
    hasDown=[]
    getAll(curs,uID,numKit,usedLev,usedParent,usedID,availNum,usedNum,reqNum,hasDown)
    lastParent=-1
    for i in range(len(usedID)):
        parentID=-1
        if(usedParent[i]!=lastParent):
            parentID=usedParent[i]
            lastParent=parentID
        if(reqNum[i]>0):
            writeLineAllcsv(curs,parentID,usedID[i],availNum[i],usedNum[i],reqNum[i])

def genKitReqOnly(conn, curs, orderRef, uID, numKit):
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
    conn = mysql.connector.connect(host="localhost",database="inventory",user="data0",password="pppp");
    curs=conn.cursor();
    genKitReq(conn,curs,"S0000",uID,numKit)
    genKitAll(conn,curs,"S0000",uID,numKit)
    conn.close()
