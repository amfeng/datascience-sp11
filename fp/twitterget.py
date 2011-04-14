import urllib2
from cElementTree import iterparse

bitlyKey = "R_e8a2096aeac748d952d5c95cef25df3d"
currPage = 1
url = "http://search.twitter.com/search.atom?q=stackoverflow&rpp=100"

FIELD_DELIMITER = unicode('\x01')
LINE_DELIMITER = unicode('\x02')

tagPrefix = "{http://www.w3.org/2005/Atom}"

buffer = "" 

def appendBuffer(text):
    global buffer
    if text == None: text = ""
    buffer += text

def appendField(text):
    global capture
    appendBuffer(text)
    appendBuffer(FIELD_DELIMITER)
    capture += 1

tempPath = "data/twitter.dat.temp"
dataPath = "data/twitter.dat"
tempOut = open(tempPath, 'w+')
out = open(dataPath, 'a+')
tempOut.write(urllib2.urlopen(url + "&page=" + str(currPage)).read())


context = iterparse(tempPath, events=("start", "end"))
context = iter(context)

# Capture mode = -1 (not capturing), 0 (capturing but don't have anything),
#                 1 (have published), 2 (have title), 3 (have author)
capture = False
for event, elem in context:
    print event, elem.tag, elem.text
    if event == "end" and elem.tag == "feed": break
    if event == "start" and elem.tag == tagPrefix + "entry":
        # Inside entry
        capture = 0 
    elif event == "end" and elem.tag == tagPrefix + "entry":
        if capture != 3: raise "Error, didn't get all of the tags before entry ended"
        appendBuffer(LINE_DELIMITER)
        capture = -1 
    else:
        # If currently capturing
        if capture >= 0 and event != "end":
            if elem.tag == tagPrefix + "published":
                if capture != 0: raise "Error, not the right place for a published tag"
                appendField(elem.text)
            elif elem.tag == tagPrefix + "title":
                # Ignore error checking for title tags, since other things can also
                # have title tags.
                #if capture != 1: raise "Error, not the right place for a title tag"
                appendField(elem.text)
            elif elem.tag == tagPrefix + "author":
                if capture != 2: raise "Error, not the right place for an author tag"
                appendField(elem.text)
            
out.write(buffer);
