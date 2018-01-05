SELECT avg(daily_total)
FROM (
    SELECT timestamp::date, COUNT(*) as daily_total
    FROM sentiment
    GROUP BY 1
    ORDER BY 1
) as x;
/* Need to use 'as x' because Postgres requires an
   identifier to the dervied table in case you make
   further constraints on it. See 
   https://stackoverflow.com/questions/14767209 for
   details.
*/
