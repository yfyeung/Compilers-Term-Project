SELECT
  r.id,
  r.uid,
  r.age ,
  r.datatime
FROM (SELECT
    id,
    uid,
    age ,
    datatime
  FROM student
  ORDER BY age DESC) r
GROUP BY r.uid
ORDER BY r.age DESC