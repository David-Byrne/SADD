# See http://pythonforengineers.com/natural-language-processing-and-sentiment-analysis-with-python/

import nltk.corpus
from nltk.corpus import twitter_samples
from nltk.classify import NaiveBayesClassifier


STOP_WORDS = nltk.corpus.stopwords.words("english")
BANNED_EMOJIS = [":)", ":(", ":-)", ":-(", ":D"]
# NLTK seemed to gather positive and negative tweets just by looking for these emojis
# so leaving them in causes the classifier to focus just on these rather than the text


def is_useful_word(word):
    if word in STOP_WORDS:
        return False
    if word.startswith(("@", "http://")):
        return False
    # If the word contains an illegal emoji, like ':)!!!'
    if any(banned in word for banned in BANNED_EMOJIS):
        return False
    return True


def create_word_features(words):
    useful_words = filter(is_useful_word, words)

    # Naive Bayes Classifier expects word:True pairs
    formatted_words = dict([(word, True) for word in useful_words])
    return formatted_words


def main():
    neg_twts = [(create_word_features(twt.split()), "negative")
                for twt in twitter_samples.strings('negative_tweets.json')]

    pos_twts = [(create_word_features(twt.split()), "positive")
                for twt in twitter_samples.strings('positive_tweets.json')]

    train_set = neg_twts[:4000] + pos_twts[:4000]
    test_set = neg_twts[1000:] + pos_twts[1000:]

    classifier = NaiveBayesClassifier.train(train_set)
    accuracy = nltk.classify.util.accuracy(classifier, test_set)
    print(accuracy)


if __name__ == '__main__':
    main()
