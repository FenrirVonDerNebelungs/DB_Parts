tablesqlstr="units"

def colFromColVal(curs,col,fromCol, val):
    inqStr="SELECT "+col+" FROM "+tablesqlstr+" WHERE "+fromCol+"=\'" + str(val)+"\'"
    curs.execute(inqStr)
    sqlout=curs.fetchone()[0]
    if not sqlout:
        return 0
    return sqlout

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

def labelsFromIDs(curs,uIDstr):
    inqStr="SELECT LABEL FROM "+tablesqlstr+" WHERE U_ID="+uIDstr
    curs.execute(inqStr)
    sqllines=curs.fetchall()
    return sqllines

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
