# Setup
Download the latest Stack Overflow dataset at <http://blog.stackoverflow.com/category/cc-wiki-dump/>
Run: 
        python xml2dat.py <PATH-TO-DATA> # this may take some time
        mysql -u <USER> -p < import.sql
        python processTags.py            # generates tags.dat
        mysql -u <USER> -p < import_tags.sql

