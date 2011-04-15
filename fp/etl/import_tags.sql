use cs194;

LOAD DATA LOCAL INFILE 'tags.dat' INTO TABLE tags FIELDS TERMINATED BY '' LINES TERMINATED BY '';

INSERT INTO toptags (Tag, Count)
    SELECT Tag, COUNT(*) as c1
        FROM tags
        GROUP BY tag
        ORDER BY c1 DESC
        LIMIT 50;

