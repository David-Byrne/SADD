import tweepy
import json


class TwitterConnector(object):
    def __init__(self):
        secrets = self.read_in_secrets()
        auth = tweepy.OAuthHandler(secrets["consumerKey"], secrets["consumerSecret"])
        auth.set_access_token(secrets["accessTokenKey"], secrets["accessTokenSecret"])
        self.api = tweepy.API(auth)

    @staticmethod
    def read_in_secrets():
        with open("secrets.json") as file:
            return json.load(file)

    def fetch_tweets(self, username, limit=300):
        # maybe look at:
        # https://github.com/tweepy/tweepy/blob/master/docs/code_snippet.rst#handling-the-rate-limit-using-cursors
        tweets = []
        for status in tweepy.Cursor(self.api.user_timeline, username, count=200).items(limit):
            tweets.append(status.text)

        return tweets


if __name__ == '__main__':
    tc = TwitterConnector()
    twts = tc.fetch_tweets("David_DByrne")
    print(len(twts))
