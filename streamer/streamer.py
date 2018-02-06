import tweepy
import json
import requests
import tweet_parsing_utils as utils
from concurrent.futures import ThreadPoolExecutor


class TwitterStreamer(tweepy.StreamListener):

    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=10)
        super().__init__()

    def on_status(self, status):

        if not utils.is_tweet_valid(status):
            return

        data = {
            "id": status.id_str,
            # convert from millisconds to correct epoch format
            "timestamp": int(status.timestamp_ms)//1000,
            "text": utils.get_tweet_text(status),
            "viewpoint": utils.get_tweet_viewpoint(status)
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

        stream = tweepy.Stream(auth=auth, listener=TwitterStreamer())
        stream.filter(track=["#savethe8th", "#repealthe8th"], async=True)


if __name__ == '__main__':
    main()
