import MySQLdb
import MySQLdb.cursors

HOST = "localhost"
USER = "root"
DB = "cs194"
OUTPUT_FILE = "tags.dat"

FIELD_DELIMITER = unicode('\x01')
LINE_DELIMITER = unicode('\x02')

output = open(OUTPUT_FILE, "w+")

query = "SELECT Tags, Id, CreationDate FROm questions";
buf = ""

connection = MySQLdb.connect(host=HOST, 
                             user=USER, 
                             db=DB, 
                             cursorclass=MySQLdb.cursors.SSCursor)
cursor = connection.cursor()
cursor.execute(query)
for row in cursor:
    # Do stuff
    tags,postid,date = row
    tags = tags.lstrip("<").rstrip(">").split("><")
    if postid == None:
        postid = 0
    for tag in tags:
        buf += FIELD_DELIMITER.join([tag, str(int(postid)), str(date)])
        buf += LINE_DELIMITER

        output.write(buf.encode('UTF-8'))
        buf = ""
        

cursor.close()
