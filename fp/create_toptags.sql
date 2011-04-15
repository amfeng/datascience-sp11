use cs194;

CREATE toptags (
    Tag VARCHAR(255),
    Count INT
);

INSERT INTO toptags (Tag, Count)
    SELECT Tag, COUNT(*) as c1
        FROM tags
        GROUP BY tag
        ORDER BY c1 DESC
        LIMIT 50;

