from nltk.corpus import stopwords as nltk_stopwords
from nltk.tokenize import TweetTokenizer
from nltk.stem.snowball import SnowballStemmer


class TweetPreprocessor(object):

    def __init__(self):
        self.tokeniser = TweetTokenizer()
        self.stemmer = SnowballStemmer("english")

        self.stop_words = nltk_stopwords.words("english") + ["RT"]
        self.banned_emojis = [":)", ":(", ":-)", ":-(", ":D"]
        # NLTK seemed to gather positive and negative tweets just by looking for these emojis
        # so leaving them in causes the classifier to focus just on these rather than the text

    def is_useful_word(self, word):
        if word in self.stop_words:
            return False
        if word.startswith(("@", "http://", "https://")):
            return False
        # If the word contains an illegal emoji, like ':)!!!'
        if any(banned in word for banned in self.banned_emojis):
            return False
        return True

    def tokenise_tweet(self, tweet):
        return self.tokeniser.tokenize(tweet.lower())

    def stem(self, word):
        return self.stemmer.stem(word)

    @staticmethod
    def strip_hash(word):
        return word.lstrip("#")

    @staticmethod
    def create_word_features(words):
        return dict([(word, True) for word in words])
