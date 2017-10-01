import tweepy
import json


def read_in_secrets():
    with open("secrets.json") as file:
        return json.load(file)


def fetch_tweets(username):
    secrets = read_in_secrets()
    auth = tweepy.OAuthHandler(secrets["consumerKey"], secrets["consumerSecret"])
    auth.set_access_token(secrets["accessTokenKey"], secrets["accessTokenSecret"])
    api = tweepy.API(auth)

    # maybe look at https://github.com/tweepy/tweepy/blob/master/docs/code_snippet.rst#handling-the-rate-limit-using-cursors
    tweets = []
    for status in tweepy.Cursor(api.user_timeline, username, count=200).items(500):
        tweets.append(status.text)
        print(status.text)

    return tweets


def main():
    tweets = fetch_tweets(username="David_DByrne")
    print(len(tweets))


if __name__ == '__main__':
    main()
