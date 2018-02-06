import json
import time
import redis
import psycopg2
import psycopg2.extras
from collections import Counter
from wordcloud import WordCloud


class Analyser(object):

    def __init__(self):
        self.db_con, self.db_cursor = self.connect_to_db()
        self.redis = redis.StrictRedis(host='cache', port=6379, db=0)
        # TODO change host to a dynamic value rather than hard coded

    def run_infinitely(self, period=60):
        while True:
            self.get_daily_avg_sentiment_by_viewpoint()
            self.prune_old_tweets()
            self.generate_word_clouds()
            time.sleep(period)

    def get_daily_avg_sentiment_by_viewpoint(self):
        with open("daily_avg_sentiment_by_viewpoint.sql") as query:
            self.db_cursor.execute(query.read())

        results = self.db_cursor.fetchall()

        vp_senti = {res.timestamp.isoformat(): round(res.avg, 5)
                    for res in results if res.viewpoint}
        vn_senti = {res.timestamp.isoformat(): round(res.avg, 5)
                    for res in results if not res.viewpoint}

        self.add_to_cache("vp:senti", vp_senti)
        self.add_to_cache("vn:senti", vn_senti)

    def prune_old_tweets(self):
        with open("prune_old_tweets.sql") as sql:
            self.db_cursor.execute(sql.read())
        self.db_con.commit()

    def generate_word_clouds(self):
        save_words = self.get_word_frequency_for_viewpoint(False)
        repeal_words = self.get_word_frequency_for_viewpoint(True)

        save_cloud = WordCloud(save_words, repeal_words)
        self.add_to_cache("vn:cloud", save_cloud.as_dict())

        repeal_cloud = WordCloud(repeal_words, save_words)
        self.add_to_cache("vp:cloud", repeal_cloud.as_dict())

    def get_word_frequency_for_viewpoint(self, viewpoint):
        self.db_cursor.execute("SELECT tweet_text "
                               "FROM tweet "
                               "WHERE viewpoint = %s",
                               (viewpoint,))
        counter = Counter()
        [counter.update(WordCloud.parse_tweet(res.tweet_text)) for res in self.db_cursor]
        return counter

    def add_to_cache(self, key, value):
        if not value:
            return
        transaction = self.redis.pipeline()
        self.redis.delete(key)
        self.redis.hmset(key, value)
        transaction.execute()

    @staticmethod
    def connect_to_db():
        with open("../secrets.json") as file:
            config = json.load(file)
            # TODO change host to a dynamic value rather than hard coded
            conn = psycopg2.connect(database="postgres", host="database",
                                    user=config["dbUser"], password=config["dbPassword"])
        cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        return conn, cur


if __name__ == '__main__':
    Analyser().run_infinitely()
