SELECT country FROM Websites
UNION
SELECT country FROM apps
ORDER BY country;