import operator
from collections import Counter
from nltk.corpus import webtext


class WordCloud(object):

    def __init__(self, wordcounts, contrast):
        rel_word_freq = self.calc_relative_word_freq(wordcounts, contrast)
        self.top_words = self.get_top_words(rel_word_freq)

    def as_dict(self):
        return {item[0]: item[1] for item in self.top_words}

    @staticmethod
    def calc_relative_word_freq(words, contrast):
        scores = {}
        for word, count in words.items():
            idf = 1 + contrast[word] + (0.1 * _normal_word_freq[word])
            scores[word] = count / idf
        return scores

    @staticmethod
    def get_top_words(words):
        sorted_words = sorted(words.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_words[:100]

    @staticmethod
    def parse_tweet(text):
        words = text.lower() \
            .replace(".", " ") \
            .replace(",", " ") \
            .replace(";", " ") \
            .replace(":", " ") \
            .replace('"', " ") \
            .replace("“", " ") \
            .replace("”", " ") \
            .replace("!", " ") \
            .replace("?", " ") \
            .replace("-", " ") \
            .replace("*", " ") \
            .replace("(", " ") \
            .replace(")", " ") \
            .replace("[", " ") \
            .replace("]", " ") \
            .replace("<", "&lt;") \
            .replace(">", "&gt;") \
            .split()
        words_wo_links = [w for w in words if not w.startswith("co/")]
        #  ^This removes Twitter shorthand URLs
        words_wo_quots = [w.strip("'‘’/") for w in words_wo_links]
        return [w for w in words_wo_quots if len(w) > 1]


_normal_word_freq = Counter()
[_normal_word_freq.update(WordCloud.parse_tweet(text.split(":", maxsplit=1)[-1]))
 for text in webtext.raw("overheard.txt").split("\n")]
