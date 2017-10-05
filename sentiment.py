# See http://pythonforengineers.com/natural-language-processing-and-sentiment-analysis-with-python/

import nltk
from nltk.corpus import stopwords as nltk_stopwords
from nltk.corpus import twitter_samples
from nltk.stem.snowball import SnowballStemmer
from nltk.classify import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB
from statistics import mean, stdev
from copy import copy


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

        all_twts = neg_twts + pos_twts

        self.classifier = SklearnClassifier(MultinomialNB(alpha=1.05))
        results = self.cross_validate(self.classifier, all_twts, 10)
        self.classifier.train(all_twts)
        print("Initialised classifier with an accuracy of {:.2f}%, +/- {:.2f}%"
              .format(mean(results) * 100, stdev(results) * 2 * 100))

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
        words_wo_hts = [word.lstrip("#") for word in words]
        useful_words = filter(self.is_useful_word, words_wo_hts)

        stemmer = SnowballStemmer("english")
        stemmed_words = [stemmer.stem(word) for word in useful_words]

        # NLTK Classifiers expect word:True pairs
        formatted_words = dict([(word, True) for word in stemmed_words])
        return formatted_words

    def classify(self, tweet):
        word_features = self.create_word_features(tweet)
        return self.classifier.classify(word_features)

    @staticmethod
    def cross_validate(algo, data, num_folds):
        results = []
        for i in range(0, num_folds):
            train_data = copy(data)
            test_data = train_data[i::num_folds]
            # stratifies the data by picking out every nth element, with increasing offset
            del train_data[i::num_folds]
            # removes the test data from the training dataset

            trained_algo = algo.train(train_data)
            accuracy = nltk.classify.util.accuracy(trained_algo, test_data)
            results.append(accuracy)

        return results


if __name__ == '__main__':
    classifier = SentimentClassifier()
