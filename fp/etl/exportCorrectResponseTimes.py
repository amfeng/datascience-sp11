import json
import MySQLdb
import MySQLdb.cursors

HOST = "localhost"
USER = "root"
DB = "cs194"
OUTFILE = "correct_responsetimes.js"

handle = open(OUTFILE, "w+")
query = "SELECT Tag, CorrectResponseTime FROM correct_responsetimes";
tags = {}

connection = MySQLdb.connect(host=HOST, 
                             user=USER, 
                             db=DB, 
                             cursorclass=MySQLdb.cursors.SSCursor)
cursor = connection.cursor()
cursor.execute(query)
for row in cursor:
    tag, correct = row
    if tag in tags:
        tags[tag].append(correct)
    else:
        tags[tag] = [correct]
       

cursor.close()

handle.write(json.dumps({"data": tags}))
handle.close()
