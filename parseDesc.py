
def funcExtract(desc):
    retArg = [desc, -1, -1]
    firstpar=desc.find("\"")
    if firstpar<0:
        return retArg
    lastpar=desc.find("\"",firstpar+1)
    nextcom=desc.find(",",lastpar)
    istailpar = (lastpar+1)==nextcom
    while not istailpar and nextcom>=0:
        nextcom=desc.find(",",lastpar)
        lastpar+=1
        istailpar= lastpar==nextcom
    if not istailpar:
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

def funcClean(desc):
    extDesc = funcExtract(desc)
    cleandDesc = funcRemDup(extDesc[0])
    return [cleandDesc,extDesc[1],extDesc[2]]

def funcFix(line):
    isoDesc = funcClean(line)
    if isoDesc[1]>=0 and isoDesc[2]>=0:
        linestrt = line[:isoDesc[1]]
        linetail = line[isoDesc[2]:]
        fixedline=linestrt+isoDesc[0]+linetail
        return fixedline
    return line