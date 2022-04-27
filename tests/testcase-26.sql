SELECT NAME,salary 
FROM employees 
WHERE salary > ALL ( SELECT salary FROM employees WHERE department_id = 6 ) 
ORDER BY salary;