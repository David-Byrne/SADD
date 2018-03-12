SELECT timestamp::date, viewpoint, COUNT(*)
FROM sentiment
GROUP BY 1, 2
ORDER BY 1, 2;
