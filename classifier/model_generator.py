import pickle
import nltk
from nltk.corpus import twitter_samples
from nltk.classify import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB
from statistics import mean, stdev
from copy import copy
from tweet_preprocessor import TweetPreprocessor


class ModelGenerator(object):

    def __init__(self):
        self.pre_pro = TweetPreprocessor()
        self.classifier = SklearnClassifier(MultinomialNB(alpha=1.375))

        neg_twts = [(self.process_tweet(twt), "negative")
                    for twt in twitter_samples.strings('negative_tweets.json')]

        pos_twts = [(self.process_tweet(twt), "positive")
                    for twt in twitter_samples.strings('positive_tweets.json')]

        all_twts = neg_twts + pos_twts

        acc_scores, confusion_matrix = self.cross_validate(self.classifier, all_twts, 10)
        self.classifier.train(all_twts)
        print("Initialised classifier with an accuracy of {:.2f}%, +/- {:.2f}%"
              .format(mean(acc_scores) * 100, stdev(acc_scores) * 2 * 100))
        print("Confusion matrix: \n{}".format(confusion_matrix))

    def process_tweet(self, tweet):
        words = self.pre_pro.tokenise_tweet(tweet)
        words_wo_htgs = [self.pre_pro.strip_hash(word) for word in words]
        useful_words = [w for w in words_wo_htgs if self.pre_pro.is_useful_word(w)]

        stemmed_words = [self.pre_pro.stem(word) for word in useful_words]
        return self.pre_pro.create_word_features(stemmed_words)

    def persist(self):
        pickle.dump(self.classifier, open("model.p", "wb"))

    @staticmethod
    def cross_validate(algo, data, num_folds):
        acc_scores = []
        predicted_results = []
        actual_results = []

        for i in range(0, num_folds):
            train_data = copy(data)
            test_data = train_data[i::num_folds]
            # stratifies the data by picking out every nth element, with increasing offset
            del train_data[i::num_folds]
            # removes the test data from the training dataset

            trained_algo = algo.train(train_data)
            accuracy = nltk.classify.util.accuracy(trained_algo, test_data)
            acc_scores.append(accuracy)

            for td in test_data:
                predicted_results.append(trained_algo.classify(td[0]))
                actual_results.append(td[1])

        confusion_mat = nltk.ConfusionMatrix(actual_results, predicted_results)
        return acc_scores, confusion_mat


if __name__ == '__main__':
    model = ModelGenerator()
    model.persist()
