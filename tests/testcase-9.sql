-------------------------------------------
-- Lecture 02 - Relational Database Language
-------------------------------------------
-- Set operations
SELECT subject.name,score.id FROM  subject LEFT JOIN score  ON subject.id = score.subject_id