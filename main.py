from collections import Counter
import sentiment
import twitter
import word_cloud


def main(handle):
    classifier = sentiment.SentimentClassifier()
    wc = word_cloud.WordCloud()

    twt_con = twitter.TwitterConnector()
    count = Counter()
    for tweet in twt_con.fetch_tweets(handle):
        res = classifier.classify(tweet)
        print(tweet)
        print(res)
        print("*****************************")
        count[res] += 1

        wc.add(tweet)

    print("\nOverall sentiment:")
    print(count)

    print("\nTop terms:")
    wc.display(limit=10)


if __name__ == '__main__':
    main("David_DByrne")
