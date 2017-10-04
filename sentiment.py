# See http://pythonforengineers.com/natural-language-processing-and-sentiment-analysis-with-python/

import nltk
from nltk.corpus import stopwords as nltk_stopwords
from nltk.corpus import twitter_samples
from nltk.stem.snowball import SnowballStemmer
from nltk.classify import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB


class SentimentClassifier(object):

    STOP_WORDS = nltk_stopwords.words("english") + ["RT"]
    BANNED_EMOJIS = [":)", ":(", ":-)", ":-(", ":D"]
    # NLTK seemed to gather positive and negative tweets just by looking for these emojis
    # so leaving them in causes the classifier to focus just on these rather than the text

    def __init__(self):
        neg_twts = [(self.create_word_features(twt), "negative")
                    for twt in twitter_samples.strings('negative_tweets.json')]

        pos_twts = [(self.create_word_features(twt), "positive")
                    for twt in twitter_samples.strings('positive_tweets.json')]

        train_set = neg_twts[:4000] + pos_twts[:4000]
        test_set = neg_twts[4000:] + pos_twts[4000:]

        self.classifier = SklearnClassifier(MultinomialNB(alpha=1.05))
        self.classifier.train(train_set)
        accuracy = nltk.classify.util.accuracy(self.classifier, test_set)
        print("Initialised Classifier with accuracy of {}%".format(accuracy*100))

    def is_useful_word(self, word):
        if word in self.STOP_WORDS:
            return False
        if word.startswith(("@", "http://", "https://")):
            return False
        # If the word contains an illegal emoji, like ':)!!!'
        if any(banned in word for banned in self.BANNED_EMOJIS):
            return False
        return True

    def create_word_features(self, tweet):
        words = tweet.lower().split()
        useful_words = filter(self.is_useful_word, words)

        stemmer = SnowballStemmer("english")
        stemmed_words = [stemmer.stem(word) for word in useful_words]

        # Naive Bayes Classifier expects word:True pairs
        formatted_words = dict([(word, True) for word in stemmed_words])
        return formatted_words

    def classify(self, tweet):
        word_features = self.create_word_features(tweet)
        return self.classifier.classify(word_features)

if __name__ == '__main__':
    classifier = SentimentClassifier()
