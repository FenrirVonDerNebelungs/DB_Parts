import mysql.connector
import blobLinks

tablesqlstr="dummytest"

def qtyFromID(uID,curs):
    inqStr="SELECT QTY FROM "+tablesqlstr+" WHERE U_ID =\'" + str(uID)+"\'"
    curs.execute(inqStr)
    sqlout=curs.fetchone()[0]
    if not sqlout:
        return 0
    return sqlout

def genSubReq(curs, uID, idUsed, numUsed, idReq, numReq):
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
        numRem=numAvail-qtyar[i]
        curNumUsed=qtyar[i]
        if(numRem<0):
            idReq.append(linksar[i])
            numReq.append(-numRem)
            if(numAvail>0):
                curNumUsed=numAvail
        if(curNumUsed>0):
            idUsed.append(linksar[i])
            numUsed.append(curNumUsed)
    return True

def writeLine(conn, curs, orderRef, lev, kitUID, uID):
    print("")

def genKitReq(conn, curs, orderRef, uID):
    idUsed=[]
    numUsed=[]
    idReq=[]
    numReq=[]
    lev=0
    goDown=True
    while goDown:
        goDown=genSubReq(curs,uID,idUsed, numUsed,idReq,numReq)
        if not goDown:
            writeLine(conn, curs, orderRef, lev, uID, -1)


conn = mysql.connector.connect(host="localhost",database="parts_test2",user="data0",password="XXfish3x3");
tablesqlstr="dummytest"

curs=conn.cursor();



conn.close()
