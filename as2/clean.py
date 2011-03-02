import re

read = open('votes.csv', 'r+')
urls = open('bad_urls.txt', 'r+')
write = open('votes_clean.csv', 'r+')

bad_urls = {}
for url in urls:
   bad_urls[url.rstrip('\n')] = 1

username_invalid = re.compile(r'^[0-9]*$')

for line in read:
    sep = line.split(",")
    name = sep[0]
    url = sep[1]
    
    #If username is valid (does not has only decimal digits) and link ID is not "bad", write to clean file
    match = username_invalid.match(name)

    if match or url in bad_urls:
        continue
    write.write(line)

