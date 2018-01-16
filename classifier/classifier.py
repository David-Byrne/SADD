import pickle
import tweet_preprocessor


class Classifier(object):

    def __init__(self):
        self.pre_pro = tweet_preprocessor.TweetPreprocessor()
        with open("model.p", mode="rb") as model_file:
            self.model = pickle.load(model_file)

    def classify(self, tweet):
        words = self.pre_pro.tokenise_tweet(tweet)
        words_wo_htgs = [self.pre_pro.strip_hash(word) for word in words]
        useful_words = [w for w in words_wo_htgs if self.pre_pro.is_useful_word(w)]

        stemmed_words = [self.pre_pro.stem(word) for word in useful_words]
        features = self.pre_pro.create_word_features(stemmed_words)
        return self.model.classify(features)
