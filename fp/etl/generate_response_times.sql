use cs194;

INSERT INTO responsetimes (QuestionId, AnswerId, Tag, ResponseTime)
    SELECT q.Id, a.Id, t.Tag, UNIX_TIMESTAMP(a.CreationDate) - UNIX_TIMESTAMP(q.CreationDate)
    FROM questions as q, answers as a, tags as t
    WHERE q.Id = a.ParentId AND t.PostId = q.Id;

INSERT INTO aggregate_responsetimes (QuestionId, Tag, AverageResponseTime, FastestResponseTime)
    SELECT r1.QuestionId, r1.Tag, AVG(r1.ResponseTime), MIN(r1.ResponseTime)
    FROM responsetimes as r1
    GROUP BY r1.QuestionId;

INSERT INTO correct_responsetimes (QuestionId, Tag, CorrectResponseTime)
    SELECT q.Id, r.Tag, r.ResponseTime
    FROM responsetimes as r, questions as q
    WHERE r.Questionid = q.Id AND q.AcceptedAnswerId = r.AnswerId
    GROUP BY q.Id, r.Tag, r.ResponseTime;
