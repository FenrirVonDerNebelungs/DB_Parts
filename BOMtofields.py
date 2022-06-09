import parseDesc

def getFields(line):
    fieldsar = ["bomdesc", "desc", 0]
    fieldsarEx=["bomdesc", "nobracbom", "A000", "desc", "nobracdesc", "A000", -1]
    fixed00=parseDesc.funcFix(line)
    fixed=parseDesc.funcFix(fixed00)
    #print(fixed)
    commaloc=fixed.find(",")
    fieldindx=0
    while commaloc>=0:
        fieldstr=fixed[:commaloc]
        fieldsar[fieldindx]=fieldstr
        #print(fieldsar[fieldindx])
        fieldindx+=1
        commaloc+=1
        remstr=fixed[commaloc:]
        fixed=remstr
        commaloc=fixed.find(",")
    if len(fixed)>1:
        fieldsar[fieldindx] = parseDesc.funcRemQuotes(fixed)
        fieldindx+=1
    fieldsarEx[0]=fieldsar[0]
    fieldsarEx[3]=fieldsar[1]
    fieldsarEx[6]=parseDesc.funcRemEndl(fieldsar[2])
    fieldsarEx[1]=parseDesc.funcClearFirstBrackets(fieldsar[0])
    #print(fieldsarEx[1])
    fieldsarEx[2]=parseDesc.funcExtractFromBrackets(fieldsar[0])
    #print(fieldsarEx[2])
    fieldsarEx[4]=parseDesc.funcClearFirstBrackets(fieldsar[1])
    #print(fieldsarEx[4])
    fieldsarEx[5]=parseDesc.funcExtractFromBrackets(fieldsar[1])
    #print(fieldsarEx[5])
    return fieldsarEx
