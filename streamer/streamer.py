import tweepy
import json
import requests
from concurrent.futures import ThreadPoolExecutor
from tweet_parsing_utils import TweetParser


class TwitterStreamer(tweepy.StreamListener):

    def __init__(self, config):
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.parser = TweetParser(config)
        super().__init__()

    def on_status(self, status):

        if not self.parser.is_tweet_valid(status):
            return

        data = {
            "id": status.id_str,
            # convert from millisconds to correct epoch format
            "timestamp": int(status.timestamp_ms)//1000,
            "text": self.parser.get_tweet_text(status),
            "viewpoint": self.parser.get_tweet_viewpoint(status)
        }

        self.executor.submit(self.send_data_onward, data)

    @staticmethod
    def send_data_onward(data):
        print(data)
        requests.post("http://classifier:8000/classify", json=data)


def main():
    with open("../secrets.json") as file:
        secrets = json.load(file)
    auth = tweepy.OAuthHandler(secrets["consumerKey"], secrets["consumerSecret"])
    auth.set_access_token(secrets["accessTokenKey"], secrets["accessTokenSecret"])

    with open("../config.json") as file:
        config = json.load(file)
    hashtag1 = config["topic1"]["name"].lower()
    hashtag2 = config["topic2"]["name"].lower()
    stream = tweepy.Stream(auth=auth, listener=TwitterStreamer(config)) # noqa: W606
    # until a new tweepy release >3.6.0 includes https://github.com/tweepy/tweepy/pull/1042
    stream.filter(track=[hashtag1, hashtag2], async=True)


if __name__ == '__main__':
    main()
