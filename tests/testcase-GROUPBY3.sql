    SELECT class, SUM(female), AVG(num)
    FROM students
    WHERE class = "CS2"
    GROUP BY class
    HAVING a = "GROUP"
    ORDER BY b