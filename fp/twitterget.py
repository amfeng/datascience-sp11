import urllib2, json, re

bitlyKey = "R_e8a2096aeac748d952d5c95cef25df3d"
currPage = 1
twitterUrl = "http://search.twitter.com/search.json?q=stackoverflow&rpp=100"
bitlyUrl = "http://api.bitly.com/v3/expand?login=amberfeng&apiKey=" + bitlyKey + "&format=txt&shortUrl=http%3A%2F%2Fbit.ly%2F"

FIELD_DELIMITER = unicode('\x01')
LINE_DELIMITER = unicode('\x02')

bitlyRegex = re.compile('http://bit\.ly/(.{6})')
stackRegex = re.compile('(http://stackoverflow\.com/questions/\d*)')

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

obj = jsonDecoder.decode(urllib2.urlopen(twitterUrl + "&page=" + str(currPage)).read())

for e in obj["results"]:
    print e["from_user"]
    print e["created_at"]
    print e["text"]
    text = e["text"]
    match = stackRegex.search(text)
    if match:
        print match.group(0)
    else:     
        match = bitlyRegex.search(text)
        if match: 
            print match.group(1)
            requestUrl = bitlyUrl + match.group(1)
            print requestUrl
            realUrl = urllib2.urlopen(bitlyUrl + match.group(1)).read()
            print realUrl



       
#out.write(buffer);
