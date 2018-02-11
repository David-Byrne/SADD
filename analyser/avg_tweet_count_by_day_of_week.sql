-- Median tweets per day of week

SELECT day, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY volume)
--This is how to calculate the median value in Postgres

FROM (
    SELECT EXTRACT(dow from timestamp) as day, COUNT(*) as volume
    FROM sentiment
    GROUP BY 1, timestamp::date
) as t

GROUP BY t.day

ORDER BY t.day;
