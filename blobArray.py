import math

def funcSet(blob, val, index):
    #print("blob", blob)
    valbin=val.to_bytes(4, byteorder='big',signed=True)
    #print("bin val len: ", len(valbin))
    if (len(valbin)) != 4:
        return False
    bloblen=len(blob)
    #print("blob len is", bloblen)
    arindex=index*4
    indexend=arindex+3
    if indexend>=bloblen:
        print("ERROR: blobArray.funcSet index out of range for blob of 4 byte ints: ", index)
        return False
    for i in range(4):
        curindex=arindex+i
        blob[curindex]=valbin[i]
    #print("reset blob", blob)
    return True

def funcLen(blob):
    bloblen=len(blob)
    if bloblen<1:
        return 0
    lastbyte=bytearray(1)
    valcnt=0
    i=0
    while i<bloblen:
        lastbyte[0]=blob[i]
        if lastbyte[0]==0xFF:
            break
        valcnt+=1
        i+=4
    return valcnt

def funcAppend(blob,val):
    hiindex=funcLen(blob)
    if hiindex<0:
        return False
    return funcSet(blob,val,hiindex)

#returns a 4 byte signed in the int
def funcGet(blob, index):
    bloblen=len(blob)
    arindex=index*4
    indexend=arindex+3
    if indexend>=bloblen:
        return -1
    blobret=bytearray(4)
    for i in range(4):
        curindex = arindex+i
        blobret[i]=blob[curindex]
    val = int.from_bytes(blobret, "big",signed=True) #big tells that the largest values start at the lower indexes
    return val
    

#clears blob to -1
def funcClear(blob):
    bloblen=len(blob)
    if bloblen<1:
        return False
    for i in range(bloblen):
        blob[i]=0xFF
    return True

#takes an integer array of values
def funcSetAr(blob, vals):
    totlen=len(vals)
    leninbytes=4*totlen
    if leninbytes>=len(blob):
        return False
    funcClear(blob)
    retok=False
    for i in range(totlen):
        retok=funcSet(blob,vals[i],i)
        if not retok:
            break
    return retok

def funcGetAr(blob):
    bloblen=len(blob)
    arlen=int(math.floor(bloblen/4))
    vals=[]
    if arlen<1:
        return vals
    for i in range(arlen):
        val=funcGet(blob,i)
        if val<0:
            break
        else:
            vals.append(val)
    return vals

def funcRemEl(blob, index):
    vals=funcGetAr(blob)
    if len(vals)<1:
        return False
    if index>=len(vals):
        return False
    vals.pop(index)
    return funcSetAr(blob,vals)
