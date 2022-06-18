
def funcExtract(desc):
    retArg = [desc, -1, -1]
    firstpar=desc.find("\"")
    if firstpar<0:
        return retArg
    lastpar=desc.find("\"",firstpar+1)
    nextcom=desc.find(",",lastpar)
    lastpar+=1
    istailpar = lastpar==nextcom
    while not istailpar and nextcom>=0:
        nextcom=desc.find(",",lastpar)
        lastpar+=1
        istailpar= lastpar==nextcom
    if not istailpar:
        return retArg
    reddesc=desc[(firstpar+1):(lastpar-1)]
    retArg=[reddesc, firstpar, lastpar]
    return retArg

def funcExtractIMB(desc):
    retArg=[desc,-1,-1]
    comloc=desc.find(",")
    foundStartPar=False
    firstpar=0
    while not foundStartPar:
        firstpar+=1
        firstpar=desc.find("\"", firstpar)
        if firstpar<0:
            return retArg
        foundStartPar=(comloc+1)==firstpar
    if foundStartPar:
        lastpar=desc.find("\"",firstpar+1)
        nextcom=desc.find(",",lastpar)
        lastpar+=1
        istailpar = lastpar==nextcom
        while not istailpar and nextcom>=0:
            nextcom=desc.find(",",lastpar)
            lastpar+=1
            istailpar= lastpar==nextcom
        if not istailpar:
            return retArg
    else:
        return retArg
    reddesc=desc[(firstpar+1):(lastpar-1)]
    retArg=[reddesc, firstpar, lastpar]
    return retArg


def funcRemDup(desc):
    parloc=desc.find("\"")
    while parloc>=0:
        parloc+=1
        nextparloc=desc.find("\"",parloc)
        if nextparloc==parloc:
            desc=desc[:parloc]+desc[(parloc+1):]
        parloc=desc.find("\"",parloc)
    return desc

def funcRemCommas(desc):
    commaloc=desc.find(",")
    while commaloc>=0:
        desc=desc[:commaloc]+desc[(commaloc+1):]
        commaloc=desc.find(",")
    return desc


def funcRemChar(desc,ch):
    qloc = desc.find(ch)
    maxindx=len(desc)-1
    while qloc>=0:
        topindx=qloc+1
        if(topindx<=maxindx):
            desc=desc[:qloc]+desc[topindx:]
        else:
            desc=desc[:qloc]
        qloc=desc.find(ch)
    return desc

def funcRemSingQuotes(desc):
    return funcRemChar(desc,"'")

def funcRemQuotes(vstr):
    return funcRemChar(vstr,"\"")

def funcRemEndl(vstr):
    eloc=vstr.find('\n')
    if(eloc<0):
        return vstr
    vstr=vstr[:eloc]
    return vstr

def funcClean(desc):
    extDesc = funcExtract(desc)
    dupRemDesc = funcRemDup(extDesc[0])
    delsingDesc=funcRemSingQuotes(dupRemDesc)
    cleanDesc=funcRemCommas(delsingDesc)
    return [cleanDesc,extDesc[1],extDesc[2]]

def funcCleanIMB(desc):
    extDesc = funcExtractIMB(desc)
    dupRemDesc = funcRemDup(extDesc[0])
    delsingDesc=funcRemSingQuotes(dupRemDesc)
    cleanDesc=funcRemCommas(delsingDesc)
    return [cleanDesc,extDesc[1],extDesc[2]]

def funcFix(line):
    isoDesc = funcClean(line)
    if isoDesc[1]>=0 and isoDesc[2]>=0:
        linestrt = line[:isoDesc[1]]
        linetail = line[isoDesc[2]:]
        fixedline=linestrt+isoDesc[0]+linetail
        return fixedline
    return line

def funcFixIMB(line):
    isoDesc = funcCleanIMB(line)
    if isoDesc[1]>=0 and isoDesc[2]>=0:
        linestrt = line[:isoDesc[1]]
        linetail = line[isoDesc[2]:]
        fixedline=linestrt+isoDesc[0]+linetail
        return fixedline
    return line


def funcClearFirstBrackets(desc):
    lastbrac=desc.find("]")
    if(lastbrac<0):
        return desc
    lastbrac+=2
    return desc[lastbrac:]

def funcExtractFromBrackets(desc):
    firstbrac=desc.find("[")
    if firstbrac<0:
        return desc
    firstbrac+=1
    desc=desc[firstbrac:]
    lastbrac=desc.find("]")
    if lastbrac<0:
        return desc
    return desc[:lastbrac]