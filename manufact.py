import mysql.connector
import math
import blobArray
import sqlQuery

tablesqlstr="units"
mantablesqlstr="rawmanufact"

manLev=[]
manID=[]
manLab=[]
manNum=[]
manTime=[]

def getRawQtyFromID(curs,rawID):
    return sqlQuery.colFromColVal(curs,"RAWQTY","RAWID",rawID)

def colFromColVal(curs,col,fromCol,val):
    inqStr="SELECT "+col+" FROM "+mantablesqlstr+" WHERE "+fromCol+"=\'" + str(val)+"\'"
    curs.execute(inqStr)
    sqlout=curs.fetchone()[0]
    if not sqlout:
        return 0
    return sqlout

def labelFromID(curs,mID):
    return colFromColVal(curs,"MANLABEL","MANID",mID)
def timeFromID(curs,mID):
    return colFromColVal(curs,"time","MANID",mID)

def getMinNumRunsForLine(blobpIDs,blobpQTYs,merID,merReq):
    pIDs=blobArray.funcGetAr(blobpIDs)
    if(len(pIDs)<=0):
        return 0
    pQTYs=blobArray.funcGetAr(blobpQTYs)
    plen=len(pIDs)
    runsReq=0
    for i in range(plen):
        if pIDs[i] in merID:
            j=merID.index(pIDs[i])
            reqQty=merReq[j]
            prunsReq=math.ceil(reqQty/pQTYs[i])
            if(prunsReq>runsReq):
                runsReq=prunsReq
    return runsReq

def getMinNumRuns(runID,runpID,runpQTY,merID,merReq):
    runLen=len(runID)
    runsReq=0
    for i in range(runLen):
        line_runsReq=getMinNumRunsForLine(runpID[i],runpQTY[i],merID,merReq)
        if(line_runsReq>runsReq):
            runsReq=line_runsReq
    return runsReq


def appendRawReqForManLine(curs, numRuns, mID, rawID, merHiLev, merLev, merID,merNum,merUsed,merReq):
    if(numRuns<=0):
        return 0
    rawQTYPerRun=getRawQtyFromID(curs,rawID)
    numberTarget = rawQTYPerRun*numRuns
    if not rawID in merID:
        merLev.append(merHiLev)
        merID.append(rawID)
        origAvail=sqlQuery.qtyFromID(curs,rawID)
        merNum.append(origAvail)
        if numberTarget<=origAvail:
            merUsed.append(numberTarget)
            merReq.append(0)
        else:
            if origAvail<0:
                origAvail=0
            merUsed.append(origAvail)
            stillReq=numberTarget-origAvail
            merReq.append(stillReq)
    else:
        j=merID.index(rawID)
        merLev[j]=merHiLev
        origAvail=merNum[j]
        if origAvail<0:
            origAvail=0
        curAvail=origAvail-merUsed[j]
        if numberTarget<=curAvail:
            merUsed[j]=merUsed[j]+numberTarget
        else:
            AdditionalReq=numberTarget-curAvail
            merReq[j]=merReq[j]+AdditionalReq
            merUsed[j]=origAvail
    return numRuns

def appendRawReqForMan(curs, numRuns, runID, runrawID, merHiLev, merLev, merID,merNum,merUsed,merReq):
    for i in range(len(runID)):
        retVal=appendRawReqForManLine(curs, numRuns, runID[i], runrawID[i], merHiLev, merLev, merID,merNum,merUsed,merReq)
        if(retVal<=0):
            return False
    return True

def addRunsForManID(curs, runID,runrawID,runpID,runpQTY,merHiLev,merLev,merID,merNum,merUsed,merReq):
    #find number of runs for a given manfactuing process
    runsReq=getMinNumRuns(runID,runpID,runpQTY,merID,merReq)
    if runsReq<=0:
        return False
    manLev.append(merHiLev)
    manID.append(runID[0])
    manLABEL = labelFromID(curs,runID[0])
    manLab.append(manLABEL)
    manNum.append(runsReq)
    estTimePerRun=timeFromID(curs,runID[0])
    estTime=estTimePerRun*runsReq
    manTime.append(estTime)
    return appendRawReqForMan(curs, runsReq, runID,runrawID,merHiLev,merLev,merID,merNum,merUsed,merReq)

def findHighestLevel(merLev):
    hiLev=0
    for i in range(len(merLev)):
        if merLev[i]>hiLev:
            hiLev=merLev[i]
    return hiLev

def addManufact(curs,merLev,merID,merNum,merUsed,merReq):
    sqlqry="SELECT MANID,RAWID,PARTID,PARTQTY FROM "+mantablesqlstr
    curs.execute(sqlqry)
    sqllines=curs.fetchall()
    runID=[]
    runrawID=[]
    runpID=[]
    runpQTY=[]
    lastrunID=-1
    manLev.clear()
    manID.clear()
    manLab.clear()
    manNum.clear()
    manTime.clear()
    merHiLev=findHighestLevel(merLev)
    for sline in sqllines:
        (mID,rawID,pID,pQTY)=sline
        if mID!=lastrunID:
            addRunsForManID(curs, runID,runrawID,runpID,runpQTY,merHiLev,merLev,merID,merNum,merUsed,merReq)
            lastrunID=mID
            runID.clear()
            runraw.clear()
            runpID.clear()
            runpQTY.clear()
        runID.append(mID)
        runrawID.append(rawID)
        runpID.append(pID)
        runpQTY.append(pQTY)
    addRunsForManID(curs, runID,runrawID,runpID,runpQTY,merHiLev,merLev,merID,merNum,merUsed,merReq)
    return manLev,manID,manLab,manNum,manTime

