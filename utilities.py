
def StringAList(list):
    if list == []:
        return '[]'
    yay =  '['
    for thing in list:
        yay += thing+'|'
    yay = yay[:-1]
    yay = yay + ']'
    return yay

def printResults(results,fields):
    if results == []:
        print 'Oops no results matching your query'
        return
    for result in results:
        print formatTheseFields(result,fields)

def formatTheseFields(result,fields):
    toPrint = ""
    fields = fields.split(',')
    for field in fields:
        field = field.strip()
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
