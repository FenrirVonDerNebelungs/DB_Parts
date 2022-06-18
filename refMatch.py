def getID(curso):
    found_ID=-1
    numFound=0
    for row in curso:
        #print(row)
        (found_ID,)=row
        numFound+=1
    if numFound>1:
        found_ID=-1
    return found_ID

def matchID(curso, tablesqlstr, desc, intref):
    found_ID=-1
    if len(desc)<2:
        return found_ID
    if len(intref)>1:
        inqStr="SELECT U_ID FROM "+tablesqlstr+" WHERE INTERNALREF =\'" + intref+"\'"
        curso.execute(inqStr)
        found_ID=getID(curso)
    if found_ID<0:
        inqStr="SELECT U_ID FROM "+tablesqlstr+" WHERE LABEL =\'"+desc+"\'"
        curso.execute(inqStr)
        found_ID=getID(curso)
    if found_ID<0:
        inqStr="SELECT U_ID FROM "+tablesqlstr+" WHERE LABEL LIKE \'%"+desc+"%\'"
        curso.execute(inqStr)
        found_ID=getID(curso)
    return found_ID