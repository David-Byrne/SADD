import classifier
from flask import Flask, request

app = Flask(__name__)
print("Loading model...")
classi = classifier.Classifier()


@app.route("/classify", methods=["POST"])
def classify_tweet():
    data = request.get_json()
    print(data["text"])
    print(classi.classify(data["text"]))

    return "OK"
