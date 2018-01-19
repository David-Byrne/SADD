import operator


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
            scores[word] = count / (contrast[word] + 1)
        return scores

    @staticmethod
    def get_top_words(words):
        sorted_words = sorted(words.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_words[:100]
