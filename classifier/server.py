import classifier
import psycopg2
import json
from flask import Flask, request


def connect_to_db():
    with open("../secrets.json") as file:
        config = json.load(file)
        conn = psycopg2.connect(database="postgres", host="database",
                                user=config["dbUser"], password=config["dbPassword"])
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    return conn, cur


app = Flask(__name__)

print("Loading model...")
classi = classifier.Classifier()
print("Connecting to DB")
db_con, cursor = connect_to_db()
print("Ready!")


@app.route("/classify", methods=["POST"])
def classify_tweet():
    data = request.get_json()

    sentiment = classi.classify(data["text"]) == "positive"

    # Splitting up command and values helps prevent SQL injection
    cursor.execute("INSERT INTO sentiment (tweet_id, sentiment, timestamp, viewpoint)"
                   "VALUES (%s, %s, to_timestamp(%s), %s);",
                   (data["id"], sentiment, data["timestamp"], data["viewpoint"]))
    cursor.execute("INSERT INTO tweet (tweet_id, tweet_text, timestamp, viewpoint)"
                   "VALUES (%s, %s, to_timestamp(%s), %s);",
                   (data["id"], data["text"], data["timestamp"], data["viewpoint"]))

    print(data["text"])
    return "OK"
