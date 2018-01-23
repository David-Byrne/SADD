DELETE FROM tweet
WHERE tweet_id NOT IN (

  (
    SELECT tweet_id
    FROM tweet
    WHERE viewpoint = FALSE
    ORDER BY timestamp DESC
    LIMIT 1000
  )

  UNION

  (
    SELECT tweet_id
    FROM tweet
    WHERE viewpoint = TRUE
    ORDER BY timestamp DESC
    LIMIT 1000
  )

);
