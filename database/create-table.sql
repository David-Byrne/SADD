CREATE TABLE sentiment(
    tweet_id text,
    sentiment boolean,
    timestamp timestamp,
    viewpoint boolean,
    PRIMARY KEY( tweet_id )
);
