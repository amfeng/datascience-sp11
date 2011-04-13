import os, sys, re
from cElementTree import iterparse
from xmlkeys import FIELD_KEYS

FIELD_DELIMITER = unicode('\x01')
LINE_DELIMITER = unicode('\x02')
path = None

handles = []
buffers = []

def initOutput():
    global handles, buffers
    handles = []
    buffers = []

def closeOutput():
    global handles, buffers
    for i in xrange(len(handles)):
        handles[i].close()

def addHandle(handle):
    global handles, buffers
    handles.append(handle)
    buffers.append("")

def appendBuffer(index, text):
    global buffers
    buffers[index] += text

def flushOutput():
    global handles, buffers
    for i in xrange(len(handles)):
        handles[i].write(buffers[i].encode('UTF-8'))
        buffers[i] = ""

def parseFile(path, source):
    global handles, buffers
    if os.path.exists(path + source + ".dat"):
        print ".dat already exists"
        return

    initOutput()
    postsFile = False
    if not source.find("posts.xml") == -1:
        if os.path.exists(path + "questions.xml.dat"):
            print "questions.xml.dat already exists"
            return
        postsFile = True
        questionsFile = open(path + "questions.xml.dat", "wb+")
        answersFile = open(path + "answers.xml.dat", "wb+")
        addHandle(questionsFile)
        addHandle(answersFile)
    else:
        outputFile = open(path + source + ".dat", "wb+")
        addHandle(outputFile)

    lineCounter = 1

    context = iterparse(path + source, events=("start", "end"))

    # turn it into an iterator
    context = iter(context)

    # get the root element
    event, root = context.next()

    for event, elem in context:
        if lineCounter % 100 == 0:
            flushOutput()
        if elem.tag == "row":
            if event == "end":
                root.clear()
            else:
                if postsFile:
                    if elem.get("PostTypeId") == "2":
                        # Answer post
                        index = 1
                        keys = FIELD_KEYS["answers.xml"]
                    else:
                        index = 0
                        keys = FIELD_KEYS["questions.xml"]
                else:
                    index = 0
                    keys = FIELD_KEYS[source]

                vals = []
                for key in keys:
                    val = elem.get(key)
                    if val == None:
                        val = "NULL"
                    vals.append(val)
                joined = FIELD_DELIMITER.join(vals)
                appendBuffer(index, joined)
                appendBuffer(index, LINE_DELIMITER)

            lineCounter += 1
    flushOutput()
    closeOutput()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        path = sys.argv[1]
        for root, dirs, files in os.walk(path):
            for f in files:
                index = f.rfind('.xml')
                if (index > 0) and (len(f) - index == 4):
                    parseFile(path, f)
                else:
                    print "Skipping:", f,
    else:
        print "SYNTAX: ./xml2dat PATH"
