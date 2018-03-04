 -- Mean tweets per hour of day
/*
SELECT x.hour, avg(hourly_totals)
FROM (
    SELECT EXTRACT(HOUR FROM timestamp) as hour, COUNT(*) as hourly_totals
    FROM sentiment
    GROUP BY 1, timestamp::date
    ORDER BY 1
) as x
GROUP BY x.hour;
*/


-- Median tweets per hour of day

SELECT hour, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY volume)
--This is how to calculate the median value in Postgres

FROM (
    SELECT EXTRACT(hour from timestamp) as hour, COUNT(*) as volume
    FROM sentiment
    GROUP BY 1, timestamp::date
) as t

GROUP BY t.hour

ORDER BY t.hour;
