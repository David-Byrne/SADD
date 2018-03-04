SELECT timestamp::date, viewpoint, AVG(sentiment::int)
FROM sentiment
GROUP BY 1, viewpoint
ORDER BY 1, viewpoint;
