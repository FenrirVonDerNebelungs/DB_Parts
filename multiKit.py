import blobLinks
import sqlQuery
import manufact
import bisect
import mysql.connector

tablesqlstr="units"

merLev=[]
merID=[]
merNum=[]
merUsed=[]
merReq=[]

def clearKits():
    merLev.clear()
    merID.clear()
    merNum.clear()
    merUsed.clear()
    merReq.clear()

def getAssIDQty(curs, uID):
    return blobLinks.getLinksQTYs(curs,tablesqlstr,uID)

def qtyFromID(curs,uID):
    qty=0
    #do the external part first, getting data either from the database or kits already merged
    if (uID in merID):
        i=merID.index(uID)
        qty=merNum[i]-merUsed[i]
    else:
        qty=sqlQuery.qtyFromID(curs,uID)
        if qty<0:
            qty=0
    return qty

def qtyFromIDnFeed(curs,uID,feedID,feedUsed,feedReq):
    merQty=qtyFromID(curs,uID)
    #now check for conflicts with other items in the same kit
    if(uID in feedID):
        i=feedID.index(uID)
        print("found in feed, at index:",uID,i)
        print(feedID,feedUsed,feedReq)
        if feedReq[i]>0:
            qty=0 #non are availabe if required were already set to pull for prev instance of part
        else:
            qty=merQty-feedUsed[i]
    return qty

def genReqArrays(curs, uID, num, ids, numUsed, numReq):
    partype=sqlQuery.typeFromID(curs,uID)
    if partype.find('MAN')>=0 or partype.find('RAW')>=0:
        return False
    linksar,qtyar=getAssIDQty(curs,uID)
    arlen=len(linksar)
    if(arlen<=0):
        return False
    for i in range(arlen):
        subPartType=sqlQuery.typeFromID(curs,linksar[i])
        if subPartType=='RAW':
            continue
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
        ids.append(linksar[i])
        numUsed.append(curNumUsed)
        numReq.append(numMissing)
    return True

def fixUsedReq(curs, feedID, feedUsed, feedReq):
    lenf=len(feedID)
    runningIDs=[]
    kitUsed=[]
    for i in range(lenf):
        totUsedForID=feedUsed[i]
        #print("ID, numUsed: ", feedID[i],feedUsed[i])
        if feedID[i] in runningIDs:
            prev_i=runningIDs.index(feedID[i])
            #print("fixUsedReq: found dup ID:"+str(feedID[i])+" cur i: "+str(i)+" prev_i: "+str(prev_i))
            dbQty=qtyFromID(curs,feedID[i])
            qtyPrevTaken=kitUsed[prev_i]
            qtyTakenTarget=qtyPrevTaken+feedUsed[i]
            if(qtyTakenTarget>dbQty):
                #print("fixing: dbQty, prevTot, prevID, curUsed, curReq",dbQty,runningIDs[prev_i],kitUsed[prev_i],feedUsed[i],feedReq[i])
                curAvailable=dbQty-qtyPrevTaken
                newTarget=feedUsed[i]+feedReq[i]
                feedReq[i]=newTarget-curAvailable
                feedUsed[i]=curAvailable
                kitUsed[prev_i]=dbQty
                #print("fixed to: used, req",feedUsed[i],feedReq[i])
            else:
                kitUsed[prev_i]+=feedUsed[i]
            #print("used so far: ",kitUsed[prev_i])
        else:
            runningIDs.append(feedID[i])
            kitUsed.append(totUsedForID)
        #print("\n---")

#parent is the UID but as a string
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
    qty=sqlQuery.qtyFromID(curs,uID)#get the qty in the database origninal number of parts
    if(qty<0):
        qty=0
    feedLev.append(0)
    feedParent.append(str(uID))
    feedID.append(uID)
    feedNum.append(qty)
    feedUsed.append(0)
    feedReq.append(0)
    #now find the number still available taking into account previous kits, the empty feed arrays won't really be used here
    qty=qtyFromID(curs,uID)
    if(qty>=num):
        feedUsed[0]=num
    else:
        feedUsed[0]=qty
        feedReq[0]=num-qty
    hasDown.append(False)
    feed_i=1
    goOn=True
    while goOn:
        lev=feedLev[ar_i]
        curUID=feedID[ar_i]
        curReq=feedReq[ar_i]
        linksar=[]
        numUsed=[]
        numReq=[]
        gotArrays=genReqArrays(curs,curUID,curReq,linksar,numUsed,numReq)
        lenLinks=0
        #print("lev, UID, len n links: ",lev, curUID, len(linksar),linksar)
        if(gotArrays):
            hasDown[ar_i]=True
            lenLinks=len(linksar)
        for i in range(lenLinks):
            qty=sqlQuery.qtyFromID(curs,linksar[i])#get the qty in the database origninal number of parts
            if(qty<0):
                qty=0
            feedLev.append(lev+1)
            feedParent.append(str(curUID))
            feedID.append(linksar[i])
            feedNum.append(qty)
            feedUsed.append(numUsed[i])
            feedReq.append(numReq[i])
            hasDown.append(False)
            feed_i+=1
        ar_i+=1
        #print("i's: ",ar_i,feed_i)
        goOn=ar_i<feed_i
    fixUsedReq(curs, feedID, feedUsed, feedReq)
    return lev

def mergeDupAll(aLev,aPar,aID,aNum,aUsed,aReq, aDown):
    alen=len(aLev)
    for i in range(alen):
        if(aLev[i]<0):
            continue
        curID=aID[i]
        for j in range(i+1,alen):
            nextID=aID[j]
            if(curID==nextID):
                #print("merging ID "+str(curID)+"  orig used: "+str(aUsed[i])+","+str(aUsed[j])+"|  orig Req: "+str(aReq[i])+","+str(aReq[j]))
                aUsed[i]=aUsed[i]+aUsed[j]
                if(aUsed[i]>aNum[i]):#these check should not actuallly be necessary
                    print("mergeDupAll WARNING:  USED EXCEEDS NUM REQUIRED!!!!!!!!!!")
                    remnant=aUsed[i]-aNum[i]
                    aUsed[i]=aNum[i]
                    aReq[i]=aReq[j]+remnant
                else:
                    aReq[i]+=aReq[j]
                if(aLev[j]<aLev[i]):
                    aLev[i]=aLev[j]
                if(aPar[i]!=aPar[j]):
                    aPar[i]+=" OR "+aPar[j]
                #print("Parent: "+aPar[i]+"   ::new Used:"+str(aUsed[i])+" |  Req:"+str(aReq[i])+"\n")
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

def combVals(indx, lev, used, req):
    if(lev>merLev[indx]):
        merLev[indx]=lev
    newUsed=merUsed[indx]+used
    if(newUsed>merNum[indx]):
        print("ERROR: combVals<mergKit<addKit: incorrect computation of used for kit at part ID:",merID[indx])
    merUsed[indx]=newUsed
    merReq[indx]=merReq[indx]+req

def appendVals(lev,ID,Num,Used,Req):
    merLev.append(lev)
    merID.append(ID)
    merNum.append(Num)
    merUsed.append(Used)
    merReq.append(Req)

#merge kit still needs to be debugged
def mergeKit(aLev,aID,aNum,aUsed,aReq):
    alen=len(aID)
    for i in range(alen):
        if aID[i] in merID:
            j=merID.index(aID[i])
            combVals(j,aLev[i],aUsed[i],aReq[i])
        else:
            appendVals(aLev[i],aID[i],aNum[i],aUsed[i],aReq[i])


def addKit(conn,curs,uID, numKit):
    #conn = mysql.connector.connect(host="localhost",database="inventory",user="data0",password="pppp")
    #curs=conn.cursor()
    feedLev=[]
    feedParent=[]
    feedID=[]
    feedNum=[]
    feedUsed=[]
    feedReq=[]
    hasDown=[]
    getAll(curs,uID,numKit,feedLev,feedParent,feedID, feedNum, feedUsed, feedReq, hasDown)
    mergeDupAll(feedLev,feedParent,feedID,feedNum,feedUsed,feedReq,hasDown)
    mergeKit(feedLev,feedID,feedNum,feedUsed,feedReq)
    #conn.close()
    return True

#########################################################################################
def sqlQueryToParentStr(sqllines):
    parStr=""
    if not sqllines:
        return parStr
    if(len(sqllines)==1):
        (line,)=sqllines[0]
        return line[:50]
    for sqline in sqllines:
        (line,)=sqline
        adline=line[:10]
        parStr+=adline+"|"
    return parStr[:50]

def writeLineKitCSV(curs, mLev, mParent, mID, mNum, mUsed, mReq):
    if mID<0:
        return False
    mLevstr=str(mLev)
    sqllines=sqlQuery.labelsFromIDs(curs,mParent)
    mParentstr=sqlQueryToParentStr(sqllines)
    mIDstr=str(mID)
    mLabstr=sqlQuery.labelFromID(curs,mID)
    mNumstr=str(mNum)
    mUsedstr=str(mUsed)
    mReqstr=str(mReq)
    locStr=sqlQuery.locFromID(curs,mID)
    print(f"{mLevstr:8}, {mParentstr:50}, {mLabstr:50}, {mIDstr:8}, {locStr:4}, {mNumstr:8}, {mUsedstr:8}, {mReqstr:8},")
    return True

def writeKitCSV(curs,armerLev,armerPar, armerID,armerNum,armerUsed,armerReq):
    merLen=len(armerID)
    if(merLen<1):
        return False
    mLevstr="Lev"
    mParentstr="Master Kit"
    mLabstr="Description"
    mIDstr="intnl ID"
    locStr="Loc"
    mNumstr="In Inv"
    mUsedstr="Used"
    mReqstr="Ad Req"
    print(f"{mLevstr:8}, {mParentstr:50}, {mLabstr:50}, {mIDstr:8}, {locStr:4}, {mNumstr:8}, {mUsedstr:8}, {mReqstr:8},")
    for i in range(merLen):
        writeLineKitCSV(curs,armerLev[i],armerPar[i], armerID[i],armerNum[i],armerUsed[i],armerReq[i])
    return True
#####

def writeLineCSV(curs, mLev, mID, mNum, mUsed, mReq):
    if mID<0:
        return False
    mLevstr=str(mLev)
    mIDstr=str(mID)
    mLabstr=sqlQuery.labelFromID(curs,mID)
    mNumstr=str(mNum)
    mUsedstr=str(mUsed)
    mReqstr=str(mReq)
    locStr=sqlQuery.locFromID(curs,mID)
    print(f"{mLevstr:8}, {mLabstr:50}, {mIDstr:8}, {locStr:4}, {mNumstr:8}, {mUsedstr:8}, {mReqstr:8},")
    return True

def writeCSV(curs,armerLev,armerID,armerNum,armerUsed,armerReq):
    merLen=len(armerID)
    if(merLen<1):
        return False
    mLevstr="Lev"
    mLabstr="Description"
    mIDstr="intnl ID"
    locStr="Loc"
    mNumstr="In Inv"
    mUsedstr="Used"
    mReqstr="Ad Req"
    print(f"{mLevstr:8}, {mLabstr:50}, {mIDstr:8}, {locStr:4}, {mNumstr:8}, {mUsedstr:8}, {mReqstr:8},")
    for i in range(merLen):
        writeLineCSV(curs,armerLev[i],armerID[i],armerNum[i],armerUsed[i],armerReq[i])
    return True

def writeLineWork(curs,mID,mLab,mNum,mTime):
    mIDstr = str(mID)
    mLabstr=mLab
    mTimestr=str(mTime)
    mNumstr=str(mNum)
    print(f"{mIDstr:8},{mLabstr:200},{mTimestr:7},{mNumstr:8},")

def writeWork(curs,armanID,armanLab,armanNum,armanTime):
    manLen=len(armanID)
    if(manLen<1):
        return False
    mIDstr="intnl ID"
    mLabstr="Work Description"
    mTimestr="Hours"
    mNumstr="Num Req"
    print(f"{mIDstr:8},{mLabstr:200},{mTimestr:7},{mNumstr:8},")
    for i in range(manLen):
        writeLineWork(curs,armanID[i],armanLab[i],armanNum[i],armanTime[i])
    return True

################################################
def showKit(uID,numKit):
    conn = mysql.connector.connect(host="localhost",database="inventory",user="data0",password="pppp");
    curs=conn.cursor()
    feedLev=[]
    feedParent=[]
    feedID=[]
    feedNum=[]
    feedUsed=[]
    feedReq=[]
    hasDown=[]
    if not getAll(curs,uID,numKit,feedLev,feedParent,feedID, feedNum, feedUsed, feedReq, hasDown):
        conn.close()
        return False
    #for debug
    #mergeDupAll(feedLev,feedParent,feedID,feedNum,feedUsed,feedReq,hasDown)
    #
    writeKitCSV(curs,feedLev,feedParent, feedID,feedNum,feedUsed,feedReq)
    conn.close()
    return True

################################################
def checkWriteMissingInv(curs, mLev, mID, mNum, mUsed, mReq):
    mLabstr=sqlQuery.labelFromID(mID)
    if(mReq<=0):
        return False
    if mLabstr.find('MAN')>=0 or mLabstr.find('ASS')>=0:
        return False
    return writeLineCSV(curs, mLev, mID, mNum, mUsed, mReq)

def writeMissingInv(curs,armerLev,armerID,armerNum,armerUsed,armerReq):
    merLen=len(armerID)
    if(merLen<1):
        return False
    mLevstr="Lev"
    mLabstr="Description"
    mIDstr="intnl ID"
    locStr="Loc"
    mNumstr="In Inv"
    mUsedstr="Used"
    mReqstr="Ad Req"
    print(f"{mLevstr:8}, {mLabstr:200}, {mIDstr:8}, {locStr:4}, {mNumstr:8}, {mUsedstr:8}, {mReqstr:8},")
    for i in range(merLen):
        checkWriteMissingInv(curs,armerLev[i],armerID[i],armerNum[i],armerUsed[i],armerReq[i])
    return True

def genLocSorted():
    mLen=len(merID)
    loc=[]
    locLev=[]
    locID=[]
    locNum=[]
    locUsed=[]
    locReq=[]
    if(mlen<1):
        return locLev,locID,locNum,locUsed,locReq
    locLev.append(merLev[0])
    locID.append(merLev[0])
    locNum.append(merNum[0])
    locUsed.append(merUsed[0])
    locReq.append(merReq[0])
    for i in range(1,mLen):
        locSQL=sqlQuery.locFromID(curs,merID[i])
        #left [i:] includes val if index starts from zero but right[:i] is not included
        #bisect will have loc>=all vals in [:i] or all values before i
        insert_i=bisect.bisect(loc,locSQL)
        loc.insert(insert_i,locSQL)
        locLev.insert(insert_i,merLev[i])
        locID.insert(insert_i,merID[i])
        locNum.insert(insert_i,merNum[i])
        locUsed.insert(insert_i,merUsed[i])
        locReq.insert(insert_i,merReq[i])
    return locLev,locID,locNum,locUsed,locReq

def dumpInvAnal(conn,curs):#assumes that addKit has already been run
    armanLev, armanID,armanLab,armanNum,armanTime = manufact.addManufact(conn,curs,merLev,merID,merNum,merUsed,merReq)
    print("_______________________________________________________________________________________")
    print("    ALL PARTS USED BY KITS ")
    print("-------------------------------------------------------------------------------------")
    locLev,locID,locNum,locUsed,locReq=genLocSorted()
    writeCSV(curs,locLev,locID,locNum,locUsed,locReq)
    #writeCSV(curs,merLev,merID,merNum,merUsed,merReq)
    print("-------------------------------------------------------------------------------------")
    print("_______________________________________________________________________________________\n")
    print("_______________________________________________________________________________________")
    print("    MISSING INVENTORY ")
    print("-------------------------------------------------------------------------------------")
    writeMissingInv(curs,merLev,merID,merNum,merUsed,merReq)
    print("-------------------------------------------------------------------------------------")
    print("_______________________________________________________________________________________\n")
    print("_______________________________________________________________________________________")
    print("    WORK REQUIRED ")
    print("-------------------------------------------------------------------------------------")
    writeWork(curs,armanID,armanLab,armanNum,armanTime)
    print("-------------------------------------------------------------------------------------")
    print("_______________________________________________________________________________________\n")

def dumpMergedKits(curs):
    print("\n\n_______________________________________________________________________________________")
    print("    ALL PARTS USED BY KITS ")
    print("-------------------------------------------------------------------------------------")
    writeCSV(curs,merLev,merID,merNum,merUsed,merReq)
    print("-------------------------------------------------------------------------------------")
    print("_______________________________________________________________________________________\n\n")