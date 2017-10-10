from collections import Counter
from operator import itemgetter
from nltk.corpus import twitter_samples
from nltk.tokenize import TweetTokenizer


class WordCloud(object):

    def __init__(self):
        tweet_data = " ".join(twitter_samples.strings("tweets.20150430-223406.json"))
        tweet_words = TweetTokenizer().tokenize(tweet_data)
        self.reference = Counter(tweet_words)
        self.words = Counter()

    def add(self, new_words):
        for word in new_words:
            self.words[word] += 1

    def display(self, limit=5):
        tf_idf = []
        for word, count in self.words.items():
            rel_freq = count/(self.reference[word] + 1)
            # adding 1 so we never end up diving by 0
            tf_idf.append((word, rel_freq))

        sorted_terms = sorted(tf_idf, key=itemgetter(1), reverse=True)
        for i in range(0, limit):
            print(sorted_terms[i])
