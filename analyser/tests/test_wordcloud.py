import unittest
import mock
import wordcloud
from collections import Counter
from wordcloud import WordCloud


class WordCloudTester(unittest.TestCase):

    ####################################
    # constructor test
    ####################################
    @mock.patch("wordcloud._normal_word_freq", Counter())
    def test_constructor(self):
        wc = WordCloud(Counter({"alpha": 10, "beta": 5}), Counter({"alpha": 4}))
        self.assertEqual([("beta", 5), ("alpha", 2)], wc.top_words)

    ####################################
    # as_dict test
    ####################################
    @mock.patch("wordcloud._normal_word_freq", Counter())
    def test_as_dict(self):
        wc = WordCloud(Counter({"alpha": 10, "beta": 5}), Counter({"alpha": 4}))
        self.assertEqual({"beta": 5, "alpha": 2}, wc.as_dict())

    ####################################
    # calc_relative_word_frequency tests
    ####################################
    @mock.patch("wordcloud._normal_word_freq", Counter())
    def test_calc_relative_word_frequency_base_case(self):
        words = {
            "alpha": 10,
            "bravo": 5
        }
        rel_word_frequency = WordCloud.calc_relative_word_freq(Counter(words), Counter())
        self.assertEqual(words, rel_word_frequency)

    @mock.patch("wordcloud._normal_word_freq", Counter())
    def test_calc_relative_word_frequency_word_in_contrast(self):
        words = {
            "alpha": 10,
        }
        rel_word_frequency = WordCloud.calc_relative_word_freq(Counter(words),
                                                               Counter({"alpha": 4}))
        self.assertEqual({"alpha": 2}, rel_word_frequency)

    @mock.patch("wordcloud._normal_word_freq", Counter({"alpha": 10}))
    def test_calc_relative_word_frequency_word_in_normal_word_freq(self):
        words = {
            "alpha": 10,
        }
        rel_word_frequency = WordCloud.calc_relative_word_freq(Counter(words), Counter())
        self.assertEqual({"alpha": 5}, rel_word_frequency)

    @mock.patch("wordcloud._normal_word_freq", Counter({"alpha": 100}))
    def test_calc_relative_word_frequency_word_in_both_documents(self):
        words = {
            "alpha": 10,
        }
        rel_word_frequency = WordCloud.calc_relative_word_freq(Counter(words),
                                                               Counter({"alpha": 9}))
        self.assertEqual({"alpha": 0.5}, rel_word_frequency)

    ####################################
    # get_top_words tests
    ####################################
    def test_get_top_words_normal_case(self):
        words = WordCloud.get_top_words({
            "A": 1,
            "B": 3,
            "C": 2
        })
        self.assertEqual([("B", 3), ("C", 2), ("A", 1)], words)

    def test_get_top_words_over_100_words(self):
        data = {str(i): i for i in range(0, 150)}
        words = WordCloud.get_top_words(data)

        self.assertEqual(100, len(words))

        expected_top_words = [(str(i), i) for i in range(149, 49, -1)]
        self.assertEqual(expected_top_words, words)

    ####################################
    # parse_tweet tests
    ####################################
    def test_parse_tweet_base_case(self):
        words = WordCloud.parse_tweet("alpha bravo charlie")
        self.assertEqual(["alpha", "bravo", "charlie"], words)

    def test_parse_tweet_upper_case(self):
        words = WordCloud.parse_tweet("ALPHA bravo cHaRlIe")
        self.assertEqual(["alpha", "bravo", "charlie"], words)

    def test_parse_tweet_with_punctuation(self):
        words = WordCloud.parse_tweet("alpha.. “bravo?” charlie’s delta! echo/2")
        self.assertEqual(["alpha", "bravo", "charlie's", "delta", "echo/2"], words)

    def test_parse_tweet_with_angle_brackets(self):
        words = WordCloud.parse_tweet("alpha <3 bravo")
        self.assertEqual(["alpha", "&lt;3", "bravo"], words)

    def test_parse_tweet_with_links(self):
        words = WordCloud.parse_tweet("alpha https://t.co/randomletters bravo")
        self.assertEqual(["alpha", "https", "bravo"], words)

    def test_parse_tweet_with_short_words(self):
        words = WordCloud.parse_tweet("I am 3 or 4 years")
        self.assertEqual(["am", "or", "years"], words)

    ####################################
    # calculate_normal_word_freq test
    ####################################
    @mock.patch("wordcloud.webtext.raw")
    def test_calculate_normal_word_freq(self, mocked_raw):
        mocked_raw.return_value = "man: Hello\n woman:HI\n man: hello again"

        normal_word_freq = wordcloud.calculate_normal_word_freq()
        self.assertEqual({"hello": 2, "hi": 1, "again": 1}, normal_word_freq)
