SELECT subject.name,score.id FROM  subject RIGHT JOIN score  on subject.id = score.subject_id;