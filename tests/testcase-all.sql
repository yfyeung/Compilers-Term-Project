SELECT * FROM table_a 
WHERE table_a.id = 1895


SELECT id AS xx1, name AS oo1 
FROM   A  AS kk

INSERT INTO users (name, age) VALUES('姚明',25)

INSERT INTO users (name, age) VALUES('华溢',21)

INSERT INTO users (name, age) VALUES('杨总',21),('昊哥',21)

UPDATE tb_courses_new
SET course_name='DB',course_grade=3.5
WHERE course_id=2 
ORDER BY teacher_id

DELETE FROM customers 
ORDER BY Name 


DELETE  a FROM tablename AS a LEFT JOIN temp_name AS b ON a.ID = b.ID WHERE b.UserID > 0;

DELETE  a FROM tablename AS a LEFT JOIN temp_name AS b ON a.ID = b.ID WHERE b.ID IS not null;

SELECT subject.name,score.id FROM  subject LEFT JOIN score  on subject.id = score.subject_id;

SELECT subject.name,score.id FROM  subject RIGHT JOIN score  on subject.id = score.subject_id;


SELECT subject.name,score.id FROM subject JOIN score  on subject.id = score.subject_id;

SELECT * FROM stu JOIN class;                 

SELECT * FROM stu JOIN class ON classid = class.id;               

SELECT id, name, MAX(daily_typing_pages)
FROM employee_tbl 
GROUP BY name

SELECT MIN(daily_typing_pages) least, MAX(daily_typing_pages) max
FROM employee_tbl

SELECT AVG(buyprice) 
FROM products
WHERE id > 10


SELECT AVG(buyprice) 
FROM products
WHERE id < 10


SELECT AVG(buyprice) 
FROM products
WHERE id = 10

SELECT AVG(buyprice) 
FROM products
WHERE id <= 10

SELECT AVG(buyprice) 
FROM products
WHERE id >= 10

SELECT AVG(buyprice) 
FROM products
WHERE id != 10

SELECT SUM(quantityOrdered ) 
FROM orderdetails 
WHERE orderNumber = 10100;


SELECT vend_id,prod_id,prod_price 
FROM products 
WHERE prod_price <= 5;

SELECT vend_id,prod_id,prod_price 
FROM products 
WHERE vend_id IN (1001,1002);


SELECT country FROM Websites
UNION
SELECT country FROM apps
ORDER BY country;


SELECT NAME,salary 
FROM employees 
WHERE salary > ALL ( SELECT salary FROM employees WHERE department_id = 6 ) 
ORDER BY salary;


SELECT region, SUM(population), SUM(area)
FROM bbc
GROUP BY region
HAVING SUM(area)>1000000

SELECT DISTINCT name
FROM stu 
where id >= 244


SELECT * 
FROM student 
WHERE id = 1 or id = 2 AND age = 20;

SELECT*
FROM  sr, cs
WHERE sr.client_snap_id = cs.id
        AND sr.b_enable = '1'


INSERT INTO emp VALUES
(4,'zs','m','2015-09-01',10000,'2015-09-01',NULL),
(5,'li','m','2015-09-01',10000,'2015-09-01',NULL),
(6,'ww','m','2015-09-01',10000,'2015-09-01',NULL);


SELECT*
FROM  sr, cs
WHERE sr.client_snap_id = cs.id
        && sr.b_enable = '1'

SELECT*
FROM  sr, cs
WHERE sr.client_snap_id = cs.id
        || sr.b_enable = '1'

SELECT NOT 10,NOT(1-1),NOT-5,NOT NULL,NOT 1+1;


SELECT 1 AND -1,1 AND 0,1 AND NULL, 0 AND NULL;

SELECT 1 && -1,1&&0,1&&NULL,0&&NULL;

SELECT 1 || -1 || 0,1||2,1||NULL,0||NULL,NULL||NULL;

SELECT 1 XOR 1,0 XOR 0,1 XOR 0,1 XOR NULL,1 XOR 1 XOR 1;



SELECT AVG(buyprice) 
FROM products
WHERE id1 - id2 < 5

SELECT AVG(buyprice) 
FROM products
WHERE pass =  TRUE

SELECT AVG(buyprice) 
FROM products
WHERE pass =  FALSE


