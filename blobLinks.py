import blobArray
import mysql.connector

def getBlob(curso, bloblab, uid, tablesqlstr):
    inqStr="SELECT "+bloblab+" FROM "+tablesqlstr+" WHERE U_ID=\'"+str(uid)+"\'"
    print(inqStr)
    curso.execute(inqStr)
    blob = curso.fetchone()[0]
    return blob

def getUber(curso, uid, tablesqlstr):
    return getBlob(curso, "UBER", uid, tablesqlstr)

def getUntr(curso, uid, tablesqlstr):
    return getBlob(curso, "UNTR", uid, tablesqlstr)

def getUntrN(curso, uid, tablesqlstr):
    return getBlob(curso, "UNTRN", uid, tablesqlstr)

def newBlob():
    uberblob=bytearray(400)
    blobArray.funcClear(uberblob)
    return uberblob

def linksToBlob(links_ar):
    unterblob=bytearray(400)
    blobArray.funcSetAr(unterblob,links_ar)
    return unterblob

def addUberLink(bomid,uberblob): #returns true if uberblob was changed
    uberlinks=blobArray.funcGetAr(uberblob)
    if(bomid in uberlinks):
        return False
    return blobArray.funcAppend(uberblob,bomid)

def getLinksQTYs(curs, sqltable, uID):
    untrblob=getUntr(curs,uID,sqltable)
    if not untrblob:
        return [],[]
    untrNblob=getUntrN(curs,uID, sqltable)
    if not untrNblob:
        return [],[]
    IDar=blobArray.funcGetAr(untrblob)
    QTYar=blobArray.funcGetAr(untrNblob)
    if not len(IDar)==len(QTYar):
        return [],[]
    return IDar,QTYar

def printSubLinks(sqltable, uid):
    retstr=""
    conn = mysql.connector.connect(host="localhost",database="inventory",user="data0",password="pppp");
    curs=conn.cursor();
    subids, subqtys=getLinksQTYs(curs,sqltable,uid)
    lenids=len(subids)
    for i in range(lenids):
        retstr+=str(subids[i])+", "
    conn.close()
    return retstr