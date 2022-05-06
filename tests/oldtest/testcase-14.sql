SELECT id, name, MAX(daily_typing_pages)
FROM employee_tbl 
GROUP BY name