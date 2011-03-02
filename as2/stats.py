import sys, time
from avro import schema, datafile, io
from math import sqrt

filetype = ''
file = ''

#Decide which file type
if len (sys.argv) > 1:
    file = sys.argv[1]
    filetype = file.split('.')[1]

start_time = time.time()
countsPerUser = {}
if filetype == "csv":
    #Collect Data
    for line in open(file, 'r+'):
        sep = line.rstrip("\n").split(",")
        user = sep[0]
        countsPerUser[user] = countsPerUser.setdefault(user, 1) + 1

else:
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
    rec_reader = io.DatumReader()
    df_reader = datafile.DataFileReader(open(file), rec_reader)

    for record in df_reader:
        user = record['user']
        countsPerUser[user] = countsPerUser.setdefault(user, 1) + 1

"""
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
"""
#Calculate Average
sum = 0
std = 0
for item in countsPerUser.items():
    sum += item[1] #Add k-v pair values = votes

average = 0
if len(countsPerUser) > 0:
    average = sum/len(countsPerUser)

#Calculate Standard Deviation
for item in countsPerUser.items():
    std += (item[1] - average)**2

stdev = sqrt(std/(len(countsPerUser)-1))

print "Mean: %d, StdDev: %d", average, stdev
print "Time taken: %d seconds", time.time() - start_time
