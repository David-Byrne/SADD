import unittest
import mock
from collections import namedtuple
from decimal import Decimal
from analyser import Analyser


@mock.patch("analyser.redis.StrictRedis")
class AnalyserTester(unittest.TestCase):
    RawAvgResult = namedtuple("RawResult", ["avg", "timestamp", "viewpoint"])

    ####################################
    # __init__ test
    ####################################
    @mock.patch("analyser.Analyser.connect_to_db")
    def test_init(self, mocked_connect, mocked_redis):
        mocked_conn = mock.MagicMock()
        mocked_cursor = mock.MagicMock()
        mocked_redis_conn = mock.MagicMock()
        mocked_connect.return_value = (mocked_conn, mocked_cursor)
        mocked_redis.return_value = mocked_redis_conn

        an = Analyser()
        mocked_redis.assert_called_once_with(host='cache', port=6379, db=0)
        self.assertEqual(mocked_conn, an.db_con)
        self.assertEqual(mocked_cursor, an.db_cursor)
        self.assertEqual(mocked_redis_conn, an.redis)
        # checks everything's set to the correct attribute

    ####################################
    # run_infinitely test
    ####################################
    @mock.patch("analyser.Analyser.connect_to_db")
    @mock.patch("analyser.Analyser.get_daily_avg_sentiment_by_viewpoint")
    @mock.patch("analyser.Analyser.prune_old_tweets")
    @mock.patch("analyser.Analyser.generate_word_clouds")
    @mock.patch("analyser.time.sleep")
    def test_run_infinitely(self, mocked_sleep, mocked_gen_wc, mocked_prune, mocked_daily_senti,
                            mocked_connect, mocked_redis):

        # Custom class used to stop the infinite loop
        class CustomExhausted(Exception):
            pass

        mocked_connect.return_value = (None, None)
        mocked_sleep.side_effect = [None, None, CustomExhausted]

        self.assertRaises(CustomExhausted, Analyser().run_infinitely)

        self.assertEqual(3, mocked_daily_senti.call_count)
        self.assertEqual(3, mocked_prune.call_count)
        self.assertEqual(3, mocked_gen_wc.call_count)
        self.assertEqual(3, mocked_sleep.call_count)

    ####################################
    # get_daily_avg_sentiment_by_viewpoint test
    ####################################
    @mock.patch("analyser.Analyser.connect_to_db")
    @mock.patch("analyser.Analyser.add_to_cache")
    @mock.patch("analyser.Analyser.smooth_results")
    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data="<SQL here>")
    def test_get_daily_avg_sentiment_by_viewpoint(self, mocked_open, mocked_smooth,
                                                  mocked_add_to_cache, mocked_connect,
                                                  mocked_redis):
        mocked_cursor = mock.MagicMock()
        mocked_timestamp = mock.MagicMock()
        mocked_timestamp.isoformat.side_effect = [
            1,
            2,
            3
        ]
        mocked_cursor.fetchall.return_value = [
            self.RawAvgResult(0.4, mocked_timestamp, True),
            self.RawAvgResult(0.5, mocked_timestamp, False),
            self.RawAvgResult(0.6, mocked_timestamp, True)
        ]
        mocked_smooth.side_effect = [
            [
                self.RawAvgResult(0.44444444, mocked_timestamp, True),
                self.RawAvgResult(0.66666666, mocked_timestamp, True)
            ], [
                self.RawAvgResult(0.55555555, mocked_timestamp, False)
            ]
        ]
        mocked_connect.return_value = (None, mocked_cursor)

        Analyser().get_daily_avg_sentiment_by_viewpoint()

        mocked_cursor.execute.assert_called_once_with("<SQL here>")
        mocked_smooth.assert_any_call([
                self.RawAvgResult(0.4, mocked_timestamp, True),
                self.RawAvgResult(0.6, mocked_timestamp, True)
        ])
        mocked_smooth.assert_any_call([
                self.RawAvgResult(0.5, mocked_timestamp, False)
        ])
        mocked_add_to_cache.assert_any_call("vp:senti", {1: 0.44444, 2: 0.66667})
        mocked_add_to_cache.assert_any_call("vn:senti", {3: 0.55556})

    ####################################
    # smooth_results test
    ####################################
    def test_smooth_results(self, _):
        smoothed = Analyser.smooth_results([self.RawAvgResult(Decimal(0.6), 1, None),
                                            self.RawAvgResult(Decimal(0.7), 2, None),
                                            self.RawAvgResult(Decimal(0.8), 3, None),
                                            self.RawAvgResult(Decimal(0.3), 4, None),
                                            self.RawAvgResult(Decimal(0.2), 5, None)])
        self.assertEqual(5, len(smoothed))

        self.assertAlmostEqual(Decimal((0.6 * 0.6) + (0.5 * 0.3) + (0.5 * 0.1)),
                               smoothed[0].avg)
        self.assertAlmostEqual(Decimal((0.7 * 0.6) + (0.56 * 0.3) + (0.5 * 0.1)),
                               smoothed[1].avg)
        self.assertAlmostEqual(Decimal((0.8 * 0.6) + (0.638 * 0.3) + (0.56 * 0.1)),
                               smoothed[2].avg)
        self.assertAlmostEqual(Decimal((0.3 * 0.6) + (0.7274 * 0.3) + (0.638 * 0.1)),
                               smoothed[3].avg)
        self.assertAlmostEqual(Decimal((0.2 * 0.6) + (0.46202 * 0.3) + (0.7274 * 0.1)),
                               smoothed[4].avg)
        self.assertEqual(1, smoothed[0].timestamp)
        self.assertEqual(2, smoothed[1].timestamp)
        self.assertEqual(3, smoothed[2].timestamp)
        self.assertEqual(4, smoothed[3].timestamp)
        self.assertEqual(5, smoothed[4].timestamp)

    ####################################
    # prune_old_tweets test
    ####################################
    @mock.patch("analyser.Analyser.connect_to_db")
    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data="<SQL here>")
    def test_prune_old_tweets(self, mocked_open, mocked_connect, mocked_redis):
        mocked_conn = mock.MagicMock()
        mocked_cursor = mock.MagicMock()
        mocked_connect.return_value = (mocked_conn, mocked_cursor)

        Analyser().prune_old_tweets()

        mocked_cursor.execute.assert_called_once_with("<SQL here>")
        mocked_conn.commit.assert_called_once_with()

    ####################################
    # generate_word_clouds test
    ####################################
    @mock.patch("analyser.Analyser.connect_to_db")
    @mock.patch("analyser.Analyser.add_to_cache")
    @mock.patch("analyser.WordCloud")
    @mock.patch("analyser.Analyser.get_word_frequency_for_viewpoint")
    def test_generate_word_clouds(self, mocked_get_w_freq, mocked_wordcloud, mocked_add_to_cache,
                                  mocked_connect, mocked_redis):
        mocked_connect.return_value = (None, None)
        mocked_get_w_freq.side_effect = [
            {"alpha": 5},
            {"beta": 2}
        ]
        # mocked_wordcloud.as_dict.side_effect = [
        #     {"alpha": 0.5},
        #     {"beta": 0.2}
        # ]
        mocked_wordcloud_obj = mock.MagicMock()
        mocked_wordcloud_obj.as_dict.side_effect = [
            {"alpha": 0.5},
            {"beta": 0.2}
        ]
        mocked_wordcloud.return_value = mocked_wordcloud_obj

        Analyser().generate_word_clouds()

        mocked_get_w_freq.assert_any_call(False)
        mocked_get_w_freq.assert_any_call(True)
        mocked_wordcloud.assert_any_call({"alpha": 5}, {"beta": 2})
        mocked_wordcloud.assert_any_call({"beta": 2}, {"alpha": 5})
        mocked_add_to_cache.assert_any_call("vn:cloud", {"alpha": 0.5})
        mocked_add_to_cache.assert_any_call("vp:cloud", {"beta": 0.2})
        # assert_called_with only remembers the most recent call,
        # hence we're using assert_any_call

    ####################################
    # get_word_frequency_for_viewpoint test
    ####################################
    @mock.patch("analyser.Analyser.connect_to_db")
    def test_get_word_frequency_for_viewpoint(self, mocked_connect, mocked_redis):
        Tweet = namedtuple("Tweet", ["tweet_text"])

        mocked_db_cursor = mock.MagicMock()
        mocked_db_cursor.__iter__.return_value = iter([Tweet("hello"), Tweet("hello again")])
        mocked_connect.return_value = (None, mocked_db_cursor)

        word_counts = Analyser().get_word_frequency_for_viewpoint(True)

        mocked_db_cursor.execute.assert_called_once_with("SELECT tweet_text "
                                                         "FROM tweet "
                                                         "WHERE viewpoint = %s", (True,))
        self.assertEqual(2, word_counts["hello"])
        self.assertEqual(1, word_counts["again"])
        self.assertEqual(0, word_counts["goodbye"])

    ####################################
    # add_to_cache test
    ####################################
    @mock.patch("analyser.Analyser.connect_to_db")
    def test_add_to_cache_normal_case(self, mocked_connect, mocked_redis):
        mocked_connect.return_value = (None, None)
        mocked_redis_conn = mock.MagicMock()
        mocked_redis_transaction = mock.MagicMock()
        mocked_redis.return_value = mocked_redis_conn
        mocked_redis_conn.pipeline.return_value = mocked_redis_transaction

        Analyser().add_to_cache("key", "value")

        mocked_redis.assert_called_once_with(host='cache', port=6379, db=0)
        mocked_redis_conn.pipeline.assert_called_once_with()
        mocked_redis_conn.delete.assert_called_once_with("key")
        mocked_redis_conn.hmset.assert_called_once_with("key", "value")
        mocked_redis_transaction.execute.assert_called_once_with()
        # Ensures the transaction was successfully created and executed

    @mock.patch("analyser.Analyser.connect_to_db")
    def test_add_to_cache_no_value(self, mocked_connect, mocked_redis):
        mocked_connect.return_value = (None, None)
        mocked_redis_conn = mock.MagicMock()
        mocked_redis_transaction = mock.MagicMock()
        mocked_redis.return_value = mocked_redis_conn
        mocked_redis_conn.pipeline.return_value = mocked_redis_transaction

        Analyser().add_to_cache("key", None)

        mocked_redis.assert_called_once_with(host='cache', port=6379, db=0)
        mocked_redis_conn.pipeline.assert_not_called()
        mocked_redis_conn.delete.assert_not_called()
        mocked_redis_conn.hmset.assert_not_called()
        mocked_redis_transaction.execute.assert_not_called()
        # Ensures nothing is added to the cache if there's no new value

    ####################################
    # connect_to_db test
    ####################################
    @mock.patch("analyser.psycopg2.connect")
    @mock.patch("builtins.open", new_callable=mock.mock_open,
                read_data='{"dbUser": "user", "dbPassword": "pass"}')
    def test_connect_to_db(self, mocked_open, mocked_connect, _):
        mocked_cursor = mock.MagicMock()
        mocked_connection = mock.MagicMock()
        mocked_connection.cursor.return_value = mocked_cursor
        mocked_connect.return_value = mocked_connection

        connection, cursor = Analyser.connect_to_db()

        self.assertEqual(mocked_connection, connection)
        self.assertEqual(mocked_cursor, cursor)
        # checking these to ensure the 2 return values are in the correct order

        mocked_connect.assert_called_once_with(database="postgres", host="database",
                                               user="user", password="pass")
        # this check ensures we're authenticating to the database correctly
