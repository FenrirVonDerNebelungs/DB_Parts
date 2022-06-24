import mysql.connector

def locFromIRef(intRef):
    loc=""
    lenR=len(intRef)
    if lenR<=0 or lenR>5:
        return loc
    let=intRef[0]
    num=intRef[1]
    goodlet=let.isalpha()
    goodnum=num.isnumeric()
    if (not goodlet) or (not goodnum):
        return loc
    return let.capitalize()+num

def sendIRefToLoc():
    tablesqlstr="units"
    conn = mysql.connector.connect(host="localhost",database="inventory",user="data0",password="pppp");
    curs=conn.cursor()
    sqlqry="SELECT U_ID,INTERNALREF FROM "+tablesqlstr
    curs.execute(sqlqry)
    sqllines=curs.fetchall()
    for sline in sqllines:
        (uID,intRef)=sline
        loc=locFromIRef(intRef)
        if(len(loc)>0):
            sqlcom="UPDATE "+tablesqlstr+" SET LOC=%s WHERE U_ID=%s"
            inargs=(loc,uID)
            print(sqlcom,inargs)
            curs.execute(sqlcom,inargs)
            conn.commit()
    conn.close()