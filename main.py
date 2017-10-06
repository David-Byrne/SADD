from collections import Counter
import sentiment
import twitter


def main(handle):
    classifier = sentiment.SentimentClassifier()
    twt_con = twitter.TwitterConnector()
    count = Counter()
    for tweet in twt_con.fetch_tweets(handle):
        res = classifier.classify(tweet)
        print(tweet)
        print(res)
        print("*****************************")
        count[res] += 1

    print(count)


if __name__ == '__main__':
    main("David_DByrne")
