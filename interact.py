import multiKit
import mysql.connector

def printHeader():
    uIDstr="U_ID"
    typstr="Type"
    locstr="Loc"
    labelstr="Description"
    qtystr="In Inv"
    odqtystr="odoo #"
    intRefstr="odoo Ref"
    print("--------------------------------------------------")
    print(f"    {uIDstr:8} |{typstr:8} |{locstr:4} |{labelstr:50} |{qtystr:8} |{odqtystr:8} |{intRefstr:8} ")

def printLineFromSQLline(sline):
    (uID,typ,loc,label,qty,odqty,intRef)=sline
    uIDstr=str(uID)
    typstr=typ
    locstr=loc
    labelstr=label
    qtystr=str(qty)
    odqtystr=str(odqty)
    intRefstr=intRef
    print(f"    {uIDstr:8} |{typstr:8} |{locstr:4} |{labelstr:50} |{qtystr:8} |{odqtystr:8} |{intRefstr:8} ")
    return uID

def printFooter():
    print("--------------------------------------------------")

def dumpAddedKitFromSqlHeader():
    uIDstr="U_ID"
    typstr="Type"
    locstr="Loc"
    labelstr="Description"
    qtystr="In Inv"
    odqtystr="odoo #"
    intRefstr="odoo Ref"
    numKitstr="Num Added"
    print("--------------------------------------------------")
    print(f"    {labelstr:50} |{qtystr:8} |{intRefstr:8} |{numKitstr:9}")

def dumpAddedKitFromSqlUID(curs, tablesqlstr,uID,numKit):
    sqlline=kitFieldsFromSqlUID(curs,tablesqlstr,uID)
    if(len(sqlline)<1):
        return False
    (uID,typ,loc,label,qty,odqty,intRef)=sqlline
    uIDstr=str(uID)
    typstr=typ
    locstr=loc
    labelstr=label
    qtystr=str(qty)
    odqtystr=str(odqty)
    intRefstr=intRef
    numKitstr=str(numKit)
    print("     ........................................................")
    print(f"    {labelstr:50} |{qtystr:8} |{intRefstr:8} |{numKitstr:9}")
    return True

def kitFieldsFromSqlUID(curs, tablesqlstr,uID):
    sqlqry="SELECT U_ID,TYPE,LOC,LABEL,QTY,ODQTY,INTERNALREF FROM "+tablesqlstr+" WHERE U_ID="+str(uID)
    curs.execute(sqlqry)
    sqlline=curs.fetchall()[0]
    if not sqlline:
        return ()
    return sqlline

def searchUID(curs,tablesqlstr,uID):
    sqlqry="SELECT U_ID,TYPE,LOC,LABEL,QTY,ODQTY,INTERNALREF FROM "+tablesqlstr+" WHERE U_ID="+str(uID)
    curs.execute(sqlqry)
    sqlline=curs.fetchall()[0]
    if not sqlline:
        return 0
    printHeader()
    printLineFromSQLline(sqlline)
    printFooter()
    return 1

def searchLabel(curs,tablesqlstr, labin):
    sqlqry="SELECT U_ID,TYPE,LOC,LABEL,QTY,ODQTY,INTERNALREF FROM "+tablesqlstr+" WHERE LABEL LIKE \'"+labin+"%\'"
    curs.execute(sqlqry)
    sqllines=curs.fetchall()
    printHeader()
    uidCollection=[]
    if sqllines:
        for sline in sqllines:
            uID=printLineFromSQLline(sline)
            uidCollection.append(uID)
    sqlqry="SELECT U_ID,TYPE,LOC,LABEL,QTY,ODQTY,INTERNALREF FROM "+tablesqlstr+" WHERE LABEL LIKE \'%"+labin+"%\'"
    curs.execute(sqlqry)
    sqllines=curs.fetchall()
    if not sqllines:
        print("NOT FOUND")
        printFooter()
        return []
    for sline in sqllines:
        uID=printLineFromSQLline(sline)
        uidCollection.append(uID)
    printFooter()
    return uidCollection

def insertLocIntoTable(conn, curs, tablesqlstr, uid, loc):
    inqStr="UPDATE "+tablesqlstr+" SET LOC="+loc+" WHERE U_ID="+str(uid)
    curs.execute(inqStr)
    conn.commit()

def getUIDInput(uIDs):
    uID_sel=uIDs[0]
    IDin=input('Select U_ID: ')
    if(len(IDin)>0):
        numIDin=int(IDin)
        if (numIDin in uIDs):
            uID_sel=numIDin
        else:
            uID_sel=-1
    return uID_sel

def inputLabelForSearch(curs,tablesqlstr):
    descFrag=input('Description search: ')
    if(len(descFrag)<1):
        print(" null string entered ")
        return -1
    print('Searching for: '+descFrag+"...")
    uIDs=searchLabel(curs,tablesqlstr,descFrag)
    numLinesRet=len(uIDs)
    if numLinesRet<=0:
        return -1
    uID_sel=uIDs[0]
    if numLinesRet>1:
        failCnt=0
        while failCnt<5:
            uID_sel=getUIDInput(uIDs)
            if uID_sel<0:
                failCnt+=1
            else:
                break
    if(uID_sel>=0):
        searchUID(curs,tablesqlstr,uID_sel)
    return uID_sel

def setLocPreConn(conn,curs,tablesqlstr):
    uID_sel=inputLabelForSearch(curs,tablesqlstr)
    if(uID_sel<0):
        return False
    inloc=input("Set Loc (str(12)): ")
    inloclen=len(inloc)
    if(inloclen>0 and inloclen<=12):
        insertLocIntoTable(conn,curs,tablesqlstr,uID_sel,inloc)
    return True

def setLoc():
    tablesqlstr="units"
    conn = mysql.connector.connect(host="localhost",database="inventory",user="data0",password="pppp");
    curs=conn.cursor()
    setLocPreConn(conn,curs,tablesqlstr)
    conn.close()

def addKitPreConn(conn,curs,tablesqlstr):
    uID_sel=inputLabelForSearch(curs,tablesqlstr)
    if(uID_sel<0):
        return -1,0
    inNumKit=input("Number of Kits? ")
    numKit=1
    if (len(inNumKit)>0) and inNumKit.isnumeric():
        numKit=int(inNumKit)
        if(numKit<1):
            numKit=0
    if(numKit>0):
        print("Number of Kits ="+str(numKit))
        multiKit.addKit(conn,curs,uID_sel,numKit)
    else:
        print("Cancel none added")
    return uID_sel,numKit
def printAddKitsKey():
    print("\n\n-------------")
    print("Select: ")
    print("  0: clear kits")
    print("  1: add kit")
    print("  2: dump results")
    print("  3: show added")
    print("  4: exit\n")


def addKits():
    tablesqlstr="units"
    conn = mysql.connector.connect(host="localhost",database="inventory",user="data0",password="pppp");
    curs=conn.cursor()
    cycCnt=0
    maxCyc=100
    maxNotRecCyc=5
    nanCyc=0
    kitUIDs=[]
    kitNums=[]
    while cycCnt<maxCyc:
        printAddKitsKey()
        mensel=input("?: ")
        if mensel=='0':
            nanCyc=0
            multiKit.clearKits()
            kitUIDs.clear()
            kitNums.clear()
            print("reset")
        elif mensel=='1':
            nanCyc=0
            uID_sel, numKit=addKitPreConn(conn,curs,tablesqlstr)
            if(numKit>0):
                kitUIDs.append(uID_sel)
                kitNums.append(numKit)
        elif mensel=='2':
            nanCyc=0
            multiKit.dumpMergedKits(curs)
        elif mensel=='3':
            nanCyc=0
            dumpAddedKitFromSqlHeader()
            for kit_i in range(len(kitUIDs)):
                dumpAddedKitFromSqlUID(curs, tablesqlstr,kitUIDs[kit_i],kitNums[kit_i])
            printFooter()
        elif mensel=='4':
            break
        else:
            nanCyc+=1
            print("      selection not recognized")
            if nanCyc>=maxNotRecCyc:
                break
    conn.close()