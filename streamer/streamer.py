import tweepy
import json
import requests
import tweet_parsing_utils as utils


class TwitterStreamer(tweepy.StreamListener):

    def on_status(self, status):

        if not utils.is_tweet_valid(status):
            return

        try:
            tweet_text = utils.get_tweet_text(status.retweeted_status)
        except AttributeError:
            tweet_text = utils.get_tweet_text(status)

        data = {
            "id": status.id_str,
            # convert from millisconds to correct epoch format
            "timestamp": int(status.timestamp_ms)//1000,
            "text": tweet_text
        }

        print(data)
        print("------------------------------------------")
        requests.post("http://localhost:5000/classify", json=data)
        # we're just printing the data for now. Eventually we'll
        # send it to the classification microservice for analysis


def main():
    with open("../secrets.json") as file:
        secrets = json.load(file)
        auth = tweepy.OAuthHandler(secrets["consumerKey"], secrets["consumerSecret"])
        auth.set_access_token(secrets["accessTokenKey"], secrets["accessTokenSecret"])

        stream = tweepy.Stream(auth=auth, listener=TwitterStreamer())
        stream.filter(track=["#savethe8th", "#repealthe8th"], async=True)


if __name__ == '__main__':
    main()
