## Streaming
This week saw the creation of the first of the microservices - the streaming
service. Using the Tweepy lib as a wrapper for the Python streaming API, I'm
currently streaming tweets that contain `#savethe8th` or `#repealthe8th`. 

I then check the language and if it's not English, I drop the tweet since the
classifier will only be trained to handle english. I'm also checking the
timezone of the tweeter and if it's set to outside Ireland I'm dropping the
tweet. This is a decision that probably needs more thinking about, do we want
to count foreign tweets or not? Leaving it in for now and it can be easily
removed at a later date if needed.

After extracting the tweet's text, (it's harder than it sounds, see the
truncating section below), I'm creating a dictionary containing the tweet's
ID, text and timestamp. This should be the only data needed for any future
processing so no point sending all the other unneeded data. Currently this
dictionary is just being printed to the console, but once the analyser
service is up and running, it'll be sent as JSON in a HTTP PUT to be 
analysed.

#### Truncating
The issue with truncating is the `status.text` field may not contain
the full tweet text, it might be cut off with '...' replacing the end. To
find the full version of the tweet, you have to go digging.

* A re-tweet can silently trunicate the tweet. The tweet will be cut off but
the truncated flag will remain false.
  * In this case always try get the original tweet. With this, treat
  it like a normal tweet (below)
* A normal tweet can be truncated if it's a 'long tweet' or they're
replying to another tweet. The flag should be set in this case.
  * It's easiest to always try read the long version of a Tweet. If that
  fails then the normal text attribute shouldn't be truncated so read that.
  * Long Tweet example: [920672283101888519](https://twitter.com/lizziemac1982/status/920672283101888519)
