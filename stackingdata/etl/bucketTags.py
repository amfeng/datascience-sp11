import json
import MySQLdb
import MySQLdb.cursors

HOST = "localhost"
USER = "root"
DB = "cs194"
OUTPUT_FILE = "bucketed_tags.js"

FIELD_DELIMITER = unicode('\x01')
LINE_DELIMITER = unicode('\x02')

objs = []

output = open(OUTPUT_FILE, "w+")

query = "SELECT YEAR(tags.CreationDate), MONTH(tags.CreationDate), tags.Tag, COUNT(*) FROM tags, toptags where tags.Tag = toptags.Tag GROUP BY YEAR(tags.CreationDate), MONTH(tags.CreationDate), tags.Tag"

connection = MySQLdb.connect(host=HOST, 
                             user=USER, 
                             db=DB, 
                             cursorclass=MySQLdb.cursors.SSCursor)
cursor = connection.cursor()
cursor.execute(query)
for row in cursor:
    year, month, tag, count = row
    obj = {
        "year": int(year),
        "month": int(month), 
        "tag": tag,
        "count": int(count)
    }
    objs.append(obj)

output.write(json.dumps({"data": objs}))
output.close()
