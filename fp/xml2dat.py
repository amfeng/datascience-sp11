import os, sys, re
from cElementTree import iterparse

FIELD_DELIMITER = unicode('\x01')
LINE_DELIMITER = unicode('\x02')
path = None

def parseFile(source):
    if os.path.exists(source + ".dat"):
        print ".dat already exists"
        return

    # get an iterable
    outputFile = open(source + ".dat", "wb+")
    lineCounter = 1
    buf = ""

    context = iterparse(source, events=("start", "end"))

    # turn it into an iterator
    context = iter(context)

    # get the root element
    event, root = context.next()
    keys = None

    for event, elem in context:
        if lineCounter % 1000 == 0:
            outputFile.write(buf.encode('UTF-8'))
            buf = ""
        if elem.tag == "row":
            if event == "end":
                root.clear()
            else:
                if keys == None:
                    keys = elem.keys()
                vals = []
                for key in keys:
                    val = elem.get(key)
                    if val == None:
                        val = "NULL"
                    vals.append(val)
                joined = FIELD_DELIMITER.join(vals)
                buf += joined
                buf += LINE_DELIMITER
            lineCounter += 1
    outputFile.close()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        path = sys.argv[1]
        for root, dirs, files in os.walk(path):
            for f in files:
                index = f.rfind('.xml')
                if (index > 0) and (len(f) - index == 4):
                    parseFile(path + f)
                else:
                    print "Skipping:", f,
    else:
        print "SYNTAX: ./xml2dat PATH"
