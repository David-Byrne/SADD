SELECT timestamp::date, viewpoint, COUNT(*)
FROM sentiment
GROUP BY 1, viewpoint
ORDER BY 1, viewpoint;
