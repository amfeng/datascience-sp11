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
    if text == None: text = "NULL"
    buffer += text

def appendField(text, last=False):
    appendBuffer(text)
    if not last: appendBuffer(FIELD_DELIMITER)

tempPath = "data/twitter.dat.temp"
dataPath = "data/twitter.dat"
tempOut = open(tempPath, 'w+')
out = open(dataPath, 'a+')

jsonDecoder = json.JSONDecoder()

for i in range(1, 10):
    obj = jsonDecoder.decode(urllib2.urlopen(twitterUrl + "&page=" + str(i)).read())

    for row in obj["results"]:
        appendField(row["from_user"])
        appendField(row["created_at"])

        text = row["text"]

        # Regex Stack Overflow URLs
        match = stackRegex.search(text)
        if match: appendField(match.group(0), True)
        else: # Check if has bit.ly URL     
            match = bitlyRegex.search(text)
            if match: 
                requestUrl = bitlyUrl + match.group(1)
                realUrl = urllib2.urlopen(bitlyUrl + match.group(1)).read()
                print realUrl

                # Make sure it matches a stack overflow address
                match = stackRegex.search(realUrl)
                
                if match: appendField(realUrl, True)
                else: appendField(None, True)
            else: # Doesn't match either of them, set URL as NULL
                appendField(None, True)
        appendBuffer(LINE_DELIMITER)

       
out.write(buffer);
