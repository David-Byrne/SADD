# Implementation

## Languages

The main language used across the entire codebase is Python 3. I chose this as it is a general purpose programming language with huge library support. It focuses on readability and succinctness. It allows you to initially develop snippets of code using the REPL shell and simple scripts, and then easily refactor it into an object orientated and module based system. This, combined with the language's high level features, make it very quick to develop in. This allowed a rapid iteration of ideas, enabling the codebase to evolve as was needed.

The secondary language used in the project was JavaScript. Given that I wanted to create an interactive, web-based visualisation, it was the obvious choice as it is the only scripting language supported by all major browsers. I could have used a language that transpiles to JavaScript, such as TypeScript, but I felt there was very little benefit unless I planned to build a much larger web-app. Although JavaScript began its life as a browser based scripting language, it has recently become popular as a server-side programming language as well. Node.js is a server-side JavaScript runtime built on top of Google Chrome's V8 JavaScript engine. This allows developers to use the same language on both front-end and back-end web development, reducing duplication of code and the overhead of context switching. This enabled me to use JavaScript rather than Python in situations where it was better suited.

## Containerisation

I also designed all the services to be able to run as Docker containers. Containers are a growing trend in the technology industry as they allow software to run in isolation from its surroundings, without the overhead of using a virtual machine. Although both my development machine and production server are running Ubuntu 16.04, allowing the pipeline to be environment-independent is still hugely beneficial. The "Dockerfile" is a set of instructions on how a Docker image should be built and how to run the software contained in it. An example Dockerfile is as follows:

``` Dockerfile
FROM python:3.6.4
COPY secrets.json /
COPY streamer/ /streamer
WORKDIR /streamer
RUN pip install -r streamer.requirements.txt
CMD ["python", "-u", "streamer.py"]
```

The `FROM` instruction tells the Docker service to start building this image on top of the Python image of version 3.6.4. Images are built as layers allowing re-use and saving storage space. The `COPY` instruction is moving the source code and secrets from the codebase into the image. This provides it with the necessary files without needing to mount the local filesystem into the container at runtime. The `WORKDIR` instruction switches the context to the directory we created in the image to store the code. The `RUN` instruction executes the command preceding it in a shell while building the image. In this case, it uses Pip, the Python dependency manager, to install the dependencies for the streamer service. Finally the `CMD` instruction declares the command that should be used to run the program the container is meant to execute. In this case, it's getting the Python interpreter to run the streamer.py file. There are many more supported Dockerfile instructions but they weren't needed by this service to allow it to run in a container. Building this image can be done by executing `docker build --file streamer/streamer.Dockerfile --tag streamer .`. To run this newly built image, execute `docker run streamer`. This will work on any host that has docker installed, regardless of environment or dependencies.

Rather than having to manage the building and running of all the Docker images manually, I added support for Docker-Compose. This is a container orchestration tool that automates the build and run lifecycle. To run the entire pipeline, simply execute `docker-compose up` and the whole system will start up. Once Docker and Docker-Compose are installed on a system, that one command is all that is needed to run the pipeline. This makes deployments completely frictionless on any OS.

## Services

### Streamer

The streamer service is the first part of the pipeline. It is written in Python as I found the Tweepy library to suit my requirements perfectly. Although Node.js's event driven, non-blocking I/O model would suit this service quite well, none of the Node.js Twitter API libraries seemed to be as stable and have as good support for streaming as Tweepy does. This swung my decision to use Python instead. The streamer service uses Tweepy to connect to the Twitter streaming API and listen for new tweets. Before connecting to Twitter however, it first reads in configuration from config files which include API keys, specific hashtags etc.

````python
def main():
    with open("../secrets.json") as file:
        secrets = json.load(file)
    auth = tweepy.OAuthHandler(secrets["consumerKey"], secrets["consumerSecret"])
    auth.set_access_token(secrets["accessTokenKey"], secrets["accessTokenSecret"])

    with open("../config.json") as file:
        config = json.load(file)
    hashtag1 = config["topic1"]["name"].lower()
    hashtag2 = config["topic2"]["name"].lower()
    stream = tweepy.Stream(auth=auth, listener=TwitterStreamer(config))
    stream.filter(track=[hashtag1, hashtag2], async=True)
````

When a new tweet is received, it is checked to make sure it is valid. This includes checks such as ensuring it's not in a foreign language (since the classifier is only trained for English text), ensuring it's not from a foreign timezone (since these Tweets are probably just noise and aren't relevant) and ensuring it contains exactly one of the required hashtags (since we can't have a Tweet that expresses both viewpoints). If the Tweet is valid, it is sent onwards to the classifier service via a POST request to the clasifier service's REST API. The streamer keeps a thread-pool of workers to send the POST request, to prevent the streamer service from becoming blocked if the classifier is slow to acknowledge the POST request.

```` python
def on_status(self, status):

    if not self.parser.is_tweet_valid(status):
        return

    data = {
        "id": status.id_str,
        # convert from millisconds to correct epoch format
        "timestamp": int(status.timestamp_ms)//1000,
        "text": self.parser.get_tweet_text(status),
        "viewpoint": self.parser.get_tweet_viewpoint(status)
    }

    self.executor.submit(self.send_data_onward, data)
````

### Classifier

The classifier service is the most technically advanced of the services. Python has many machine learning and natural language processing (NLP) libraries making it one of the most popular languages for data science, so I chose it for this service. When its docker image is being built, it trains a machine learning model using a corpus of positive and negative Tweets supplied by the Natural Language Tool Kit (NLTK) library. For more information on the machine learning aspect, see the machine learning section of the report.

```` python
neg_twts = [(self.process_tweet(twt), "negative")
            for twt in twitter_samples.strings('negative_tweets.json')]

pos_twts = [(self.process_tweet(twt), "positive")
            for twt in twitter_samples.strings('positive_tweets.json')]

all_twts = neg_twts + pos_twts
self.classifier.train(all_twts)
````

The classifier service is run using Gunicorn. This allows us to run multiple instances of the service that all listen at the same port. When an instance of the service is started up, it loads in the serialised machine learning model from disk and establishes a connection to the database service. It then listens for POST requests from the streamer service. When it receives one, it extracts the Tweet data and classifies it using the model generated earlier. It then inserts the Tweet details and predicted sentiment into the database.

```` python
@app.route("/classify", methods=["POST"])
def classify_tweet():
    data = request.get_json()

    sentiment = classi.classify(data["text"]) == "positive"

    # Splitting up command and values helps prevent SQL injection
    cursor.execute("INSERT INTO sentiment (tweet_id, sentiment, timestamp, viewpoint)"
                   "VALUES (%s, %s, to_timestamp(%s), %s);",
                   (data["id"], sentiment, data["timestamp"], data["viewpoint"]))
````

### Database

The database is PostgresSQL, an open-source, object-relational database management system. I chose PostgresSQL because it is free, scalable and focuses on standards compliance. The table that stores the classified sentiment data contains 4 columns: the Tweet ID (also being used as primary key), the Tweet timestamp, the Tweet viewpoint and its sentiment.

````
Table "sentiment"
======================================================
COLUMN | tweet_id | sentiment | timestamp | viewpoint
-------+----------+-----------+-----------+-----------
TYPE   | text     | boolean   | timestamp | boolean

````

If we ever need to re-calculate sentiment at any point, we can re-fetch the Tweet's text from the Twitter API using its ID. This removes the need to store the text for every tweet. A second table is used to store the text from some tweets, but only the last 1000 from each viewpoint, since that's all that's needed to create the word clouds. This table is quite similar to the previous one, except we're storing the Tweet's text rather than its sentiment.

The analyser service runs various analytics across the data in the database and stores the results in the cache. Python's huge library support and ease of prototyping made it the obvious choice. I use the Psycopg2 and Redis libraries to connect to the database and cache. All the queries to fetch information from the database are written in SQL, as it's the query language supported by PostgresSQL. To generate the data for the daily sentiment visualisation, the service runs an SQL query to calculate the average daily sentiment, grouped by viewpoint. This data is quite noisy however with large fluctuations, so we calculate a weighted moving average that takes the previous days sentiment into account when generating that day's figure. A hashmap for each viewpoint with the date as the key and the sentiment score as the value is then stored into the cache. To calculate the data for the wordcloud, the last 1000 Tweets from each viewpoint are retrieved from the database and split into words. The number of occurrences of each word is calculated per viewpoint. To generate the scoring, a TF-IDF style approach is used in which the term frequency for a viewpoint is divided by the document frequency. The 'document' in this case is made up of all the Tweets from the opposing viewpoint, as well as a corpus of conversations supplied by the NLTK library. This allows us to find contrast in the language used by each viewpoint while also reducing the score of words that are commonly used in conversation, as they would likely not give us any insight into the debate. The top 100 scoring terms for each viewpoint are used to create hashmaps with the word as the key and the score as the value. These hashmaps are then inserted into the cache. These analytics are re-generated regularly to keep the results data up to date.

The cache is implemented using Redis, an open-source, in-memory data-structure store. Its simple command based language and high performance made it the ideal choice for this service. It also supports key-space notifications, which are publish-subscribe (pub-sub) channels that receive event-messages every time a value is updated. This allows the websocket to be informed as soon as the analyser pushes new results to the cache in a highly efficient and performant manner.

The websocket service is written in JavaScript using Node.js, since its event based model matches the service's main use cases. It uses the Redis and WS libraries to connect to the cache and create a websocket. When it is started up, it connects to the cache and subscribes to messages about any updates that occur. Whenever a value in the cache is updated by the analyser, it is notified of the change and it broadcasts the new value to all connected clients. When a new client connects, it queries the cache for the latest results and sends them directly to the new client.

The web service is powered by an Nginx server. I chose Nginx as it is highly performant and it maintains a low memory footprint under load. All the resources it serves are static, i.e. they don't need to be dynamically created using a server side programming language such as PHP. This is done by sending a HTML page that, when it loads, immediately connects to the websocket service. It receives the latest data when it connects and uses it to inflate the visualisations. To display the chart of sentiment levels over time, we're using the Chart.js library to create the graph. The data is scaled from the range [0,1] to [-1,1] as a symmetrical scoring system was found to be more user friendly. The values are rounded to 3 decimal places to prevent irrational numbers taking up too much space. To create the word clouds, we're using the WordCloud2.js library. We're sorting the words based on their score, ensuring the largest words are painted first. As the library starts painting from the center and keeps moving outwards until it finds space for a word, this ensures a good spread across the canvas with the most important term being in the center. The sizing of the word directly corresponds to the score it was given back in the analyser service. The sizing is scaled logarithmically however, or else the most frequent terms would be too large for the canvas and the less common terms would be illegibly small. Before repainting, the new data is compared with the old data to check if a sufficiently large change has taken place. This is done because, unlike the sentiment chart library, the word cloud library doesn't support dynamic changes without an entire repaint of the canvas. If only 2 words have swapped places in the top 100 words, there's no point triggering an entire repaint. If a large change takes place however, it's worth triggering the repaint. Each of the terms is also a link to the relevant Tweets in which it appears. This is done by dynamically building a link to a Twitter search, containing the term specified as well as the main term in the word cloud, which ensures the context is correct. This is extremely useful to clarify the context of any ambiguous or surprising terms.
