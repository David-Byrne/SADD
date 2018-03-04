SELECT timestamp::date, COUNT(*)
FROM sentiment
GROUP BY 1
ORDER BY 1;
