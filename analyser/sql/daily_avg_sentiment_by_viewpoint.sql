SELECT timestamp::date, viewpoint, AVG(sentiment::int)
FROM sentiment
GROUP BY 1, 2
ORDER BY 1, 2;
