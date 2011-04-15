use cs194;

INSERT INTO responsetimes (QuestionId, AnswerId, Tag, ResponseTime)
    SELECT q.Id, a.Id, t.Tag, UNIX_TIMESTAMP(a.CreationDate) - UNIX_TIMESTAMP(q.CreationDate)
    FROM questions as q, answers as a, tags as t
    WHERE q.Id = a.ParentId AND t.PostId = q.Id;

