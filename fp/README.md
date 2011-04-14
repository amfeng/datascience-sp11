# Setup
* Download the latest Stack Overflow dataset at http://
* Run: "python xml2dat.py <PATH-TO-DATA>" to convert the XML files to MySQL compatible .dat files
* Run import.sql to import them into your MySQL installation
* To populate the "tags" table, run "python processTags.py" which generates tags.dat, then import them with import_tags.sql

