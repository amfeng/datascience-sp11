USE cs194;

SELECT CHAR_LENGTH(q.Body), r.CorrectResponseTime
FROM questions as q, correct_responsetimes as r
WHERE q.Id = r.QuestionId
INTO OUTFILE '/tmp/correct_response_time_vs_body_length.csv'
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';
