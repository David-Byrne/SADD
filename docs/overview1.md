## Twitter integration

To collect Twitter data, I'm currently using the [Tweepy](http://www.tweepy.org/)
library. They wrap around the Twitter REST API and provide access to the various
endpoints, including the `user_timeline` endpoint, which is what I'm using to get
a person's last N tweets. 

They also provide a generic `Cursor` object which handles making multiple
requests when a single request can't return all the requested data.

If we end up switching to a real-time approach, we'll need to use the Twitter
Streaming API. Tweepy also provides a wrapper around this API so we shouldn't
need to replace it in the near future.


## Sentimenet Analysis

I'm using the [NLTK library](http://www.nltk.org/) in Python to support the
sentiment analysis I'm running. It supports many of the most common techniques
used when dealing with natural language including stemming, tokenisers, stop-word
removal, classifiers... It also comes with a 10,000 Tweet corpus with 5000 Tweets
labelled `positive` and a further 5000 labeled `negative`.

To preapare each Tweet, I'm:
* Converting it to lower case
* Splitting it into individual words
* Stripping out the "#" from hashtags
* Removing stop words, including Twitter specific stop words like "RT"
* Removing links and other user's handles
* Removing certain emojis that the classifier would depend on otherwise
* Stemming each word using NLTK's Snowball Stemmer

After all the Tweets have been prepared, I train a classifier and test it using
10-fold cross validation. Currently the best I've achieved is from using
Scikit-learn's Multinomial Naive Bayes classification algorithm, with an
estimated accuracy of 78.09%, +/- 2.20%. It was very fast to train which speeds
up development time, as well as using less laptop battery. 

Other well performing algorithms I tried were:
* MLP Neural Network Classifier with alpha = 0.9: 
  * Accuracy was 77.95%, +/- 2.98%
  * Took much longer to train than Naive Bayes
* NuSVC with linear kernal:
  * Accuracy was 78.11%, +/- 2.78%
  * Slightly higher accuracy but much less reliability
  * Training is also much more CPU intensive than the Naive Bayes
* Logistic Regression:
  * Accuracy was 78.06%, +/- 2.44%
  * Roughly as fast as Naive Bayes for training
