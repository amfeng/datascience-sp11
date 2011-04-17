import json
import MySQLdb
import MySQLdb.cursors

HOST = "localhost"
USER = "root"
DB = "cs194"
OUTFILE = "responsetimes.js"

handle = open(OUTFILE, "w+")
query = "SELECT Tag, ResponseTime FROM responsetimes";
tags = {}

connection = MySQLdb.connect(host=HOST, 
                             user=USER, 
                             db=DB, 
                             cursorclass=MySQLdb.cursors.SSCursor)
cursor = connection.cursor()
cursor.execute(query)
for row in cursor:
    tag, responsetime = row
    if tag in tags:
        tags[tag].append(responsetime)
    else:
        tags[tag] = [responsetime]
       

cursor.close()

handle.write(json.dumps({"data": tags}))
handle.close()
