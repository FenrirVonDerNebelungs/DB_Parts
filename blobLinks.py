import blobArray

def linksToBlob(bomid, links_ar):
    unterblob=bytearray(400)
    blobArray.funcSetAr(unterblob,links_ar)
    return unterblob

def addUberLink(uberblob): #returns true if uberblob was changed
    if len(uberblob)<4:
        return False
    uberlinks=blobArray.funcGetAr(uberblob)
    if(bomid in uberlinks):
        return False
    blobArray.funcAppend(uberblob,bomid)
    return True