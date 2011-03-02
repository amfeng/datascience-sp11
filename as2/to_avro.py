import sys, time
from avro import schema, datafile, io

INPUT_FILE = 'votes_clean.csv'
OUTPUT_FILE = 'votes_clean.avro'
OUTPUT_COMPR_FILE = 'votes_clean.avroc'
compr = False

#Parsing command line arguments to decide to compress or not
if len (sys.argv) > 1:
    arg = sys.argv[1]
    if arg == '-c':
        compr = True

SCHEMA_STR = """{
    "type": "record",
    "name": "votes",
    "namespace": "cs194-16",
    "fields": [
        {   "name": "user"   , "type": "string"   },
        {   "name": "url"    , "type": "string"   },
        {   "name": "vote"   , "type": "int"      }
        ]
    }"""
SCHEMA = schema.parse(SCHEMA_STR)

data = {}
rec_writer = io.DatumWriter(SCHEMA)
df_writer = None

read = open('votes_clean.csv', 'r+')

if compr: #Compressed avro format
    df_writer = datafile.DataFileWriter(
        open(OUTPUT_COMPR_FILE, 'wb'),
        rec_writer,
        writers_schema = SCHEMA,
        codec = 'deflate')
else: #Uncompressed avro format
    df_writer = datafile.DataFileWriter(
        open(OUTPUT_FILE, 'wb'),
        rec_writer,
        writers_schema = SCHEMA,
        codec = 'null')

start_time = time.time()
for line in read:
    #print line
    sep = line.rstrip('\n').split(",")
    data['user'] = sep[0]
    data['url'] = sep[1]
    data['vote'] = int(sep[2])

    df_writer.append(data)

df_writer.close()

print "Time taken: %d seconds",  time.time() - start_time
