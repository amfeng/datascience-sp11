use cs194;

CREATE INDEX tags_postid on tags(PostId);
CREATE INDEX resptimes_q on responsetimes(QuestionId);
CREATE INDEX resptimes_a on responsetimes(AnswerId);

