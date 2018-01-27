SELECT daily_tweet_count.timestamp,
       daily_tweet_count.viewpoint,
       daily_tweet_count.count / avg_daily_tweet_count_by_viewpoint.average

FROM
  (
      SELECT timestamp::date, viewpoint, COUNT(*) as count
      FROM sentiment
      GROUP BY timestamp::date, viewpoint
  ) as daily_tweet_count
  ,
  (
      SELECT avg(daily_total) as average, x.viewpoint
      FROM (
            SELECT COUNT(*) as daily_total, viewpoint
            FROM sentiment
            GROUP BY timestamp::date, viewpoint
      ) as x
      GROUP BY x.viewpoint
  ) as avg_daily_tweet_count_by_viewpoint

WHERE avg_daily_tweet_count_by_viewpoint.viewpoint = daily_tweet_count.viewpoint

ORDER BY 1, 2;
