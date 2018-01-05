import json
import time
import redis
import psycopg2
import psycopg2.extras


class Analyser(object):

    def __init__(self):
        self.db_con, self.db_cursor = self.connect_to_db()
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
        # TODO change host to a dynamic value rather than hard coded

    def run_infinitely(self, period=60):
        while True:
            self.get_daily_avg_sentiment_by_viewpoint()
            time.sleep(period)

    def get_daily_avg_sentiment_by_viewpoint(self):
        with open("daily_avg_sentiment_by_viewpoint.sql") as query:
            self.db_cursor.execute(query.read())

        results = self.db_cursor.fetchall()

        vp_senti = {res.timestamp.isoformat(): round(res.avg, 5)
                    for res in results if res.viewpoint}
        vn_senti = {res.timestamp.isoformat(): round(res.avg, 5)
                    for res in results if not res.viewpoint}

        self.redis.hmset("vp:senti", vp_senti)
        self.redis.hmset("vn:senti", vn_senti)
        self.redis.set("lastUpdated", time.time())

    @staticmethod
    def connect_to_db():
        with open("../secrets.json") as file:
            config = json.load(file)
            # TODO change host to a dynamic value rather than hard coded
            conn = psycopg2.connect(database="postgres", host='localhost',
                                    user=config["dbUser"], password=config["dbPassword"])
        cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        return conn, cur


if __name__ == '__main__':
    Analyser().run_infinitely()