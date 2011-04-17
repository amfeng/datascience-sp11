import json
import MySQLdb
import MySQLdb.cursors

HOST = "localhost"
USER = "root"
DB = "cs194"
OUTFILE = "aggregate_responsetimes.js"

handle = open(OUTFILE, "w+")
query = "SELECT Tag, AverageResponseTime, FastestResponseTime FROM aggregate_responsetimes";
tags = {}

connection = MySQLdb.connect(host=HOST, 
                             user=USER, 
                             db=DB, 
                             cursorclass=MySQLdb.cursors.SSCursor)
cursor = connection.cursor()
cursor.execute(query)
for row in cursor:
    tag, average, fastest = row
    if tag in tags:
        tags[tag][0].append(average)
        tags[tag][1].append(fastest)
    else:
        tags[tag] = [[average], [fastest]]
       

cursor.close()

handle.write(json.dumps({"data": tags}))
handle.close()
