import json
import psycopg2
import matplotlib as mpl
mpl.use('Agg')
# Setting MPL to use AGG since default backend needs an X-server, which
# won't be on the server. Needs to be initialised before importing pyplot
import matplotlib.pyplot as plt  # noqa: 402
import matplotlib.dates as mdates  # noqa: 402


class StaticAnalyser(object):

    def __init__(self):
        self.db_con, self.db_cursor = self.connect_to_db()

    def get_daily_tweet_count(self):
        with open("daily_tweet_count.sql") as query:
            self.db_cursor.execute(query.read())

        results = self.db_cursor.fetchall()
        self.plot("daily_tweet_count",
                  x=[res[0] for res in results],
                  ys=[[res[1] for res in results]],
                  legend=["Tweets Collected by Day"])

    def get_daily_tweet_count_by_viewpoint(self):
        with open("daily_tweet_count_by_viewpoint.sql") as query:
            self.db_cursor.execute(query.read())

        results = self.db_cursor.fetchall()
        self.plot("daily_tweet_count_by_viewpoint",
                  x=[res[0] for res in results if res[1]],
                  ys=[[res[2] for res in results if res[1]],
                      [res[2] for res in results if not res[1]]],
                  legend=["Pro-Choice Tweets", "Pro-Life Tweets"])

    def get_daily_avg_sentiment_by_viewpoint(self):
        with open("daily_avg_sentiment_by_viewpoint.sql") as query:
            self.db_cursor.execute(query.read())

        results = self.db_cursor.fetchall()
        self.plot("daily_avg_sentiment_by_viewpoint",
                  x=[res[0] for res in results if res[1]],
                  ys=[[res[2] for res in results if res[1]],
                      [res[2] for res in results if not res[1]]],
                  legend=["Pro-Choice Tweets", "Pro-Life Tweets"])

    @staticmethod
    def plot(image_name, x, ys, legend):
        fig, ax = plt.subplots(figsize=(15, 8))
        for y in ys:
            ax.plot(x, y)

        ax.xaxis.set_major_locator(mdates.WeekdayLocator())
        ax.xaxis.set_minor_locator(mdates.DayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

        datemin = x[0]
        datemax = x[-1]
        ax.set_xlim(datemin, datemax)

        ax.tick_params(axis='x', length=7)
        fig.autofmt_xdate()

        plt.legend(legend, loc="upper left")
        plt.savefig(image_name + ".png")

    @staticmethod
    def connect_to_db():
        with open("../secrets.json") as file:
            config = json.load(file)
            # TODO change host to a dynamic value rather than hard coded
            conn = psycopg2.connect(database="postgres", host='localhost',
                                    user=config["dbUser"], password=config["dbPassword"])
        cur = conn.cursor()
        return conn, cur


if __name__ == '__main__':
    sa = StaticAnalyser()
    sa.get_daily_tweet_count()
    sa.get_daily_tweet_count_by_viewpoint()
    sa.get_daily_avg_sentiment_by_viewpoint()