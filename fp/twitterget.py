import urllib2
import json

bitlyKey = "R_e8a2096aeac748d952d5c95cef25df3d"
currPage = 1
url = "http://search.twitter.com/search.json?q=stackoverflow&rpp=100"

FIELD_DELIMITER = unicode('\x01')
LINE_DELIMITER = unicode('\x02')

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

jsonDecoder = json.JSONDecoder()

obj = jsonDecoder.decode(urllib2.urlopen(url + "&page=" + str(currPage)).read())

for e in obj["results"]:
    print e["from_user"]
    print e["created_at"]
    print e["text"]



       
#out.write(buffer);
