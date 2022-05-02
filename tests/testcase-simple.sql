SELECT
  r.id,
  r.uid,
  r.age ,
  r.datatime
FROM Table1
GROUP BY r.uid
ORDER BY r.age