
def StringAList(list):
    yay =  '['
    for thing in list:
        yay += thing+'|'
    yay = yay[:len(yay)-1]
    yay += ']'
    return yay

def formatTheseFields(result,fields):
    toPrint = ""
    for field in fields:
        if field != 'tags':
            toPrint += result[field]+" | "
        else:
            toPrint += StringAList(result[field])+" | "
    return toPrint[:-2]

def writeToLog(goodlogfile,goodlog,badlogfile,badlog):
    good = open(goodlogfile,"r+")
    bad = open(badlogfile,"r+")
    good.write(goodlog)
    bad.write(badlog)
    good.close()
    bad.close()
