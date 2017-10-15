## Word Clouds
To get an insight into the most popular topics, I create a word cloud based
on the contents of the tweets. Currently, I'm using the NLTK's Twitter
corpus as the reference dataset. Using a TF-IDF style approach, I find the
most popular terms in the new Twitter data by dividing the count of their
occurances in the new dataset by their count in the reference dataset.

This negates the need to remove stop words and other common terms on Twitter
as they're given a low score by their popularity in the reference dataset.

#### Usernames

I'm currently removing usernames as people tend to tweet at the same
accounts frequently (giving them a high TF score) and these account often
don't appear in the reference dataset at all (giving them a high IDF score).
An example of this is someone Tweeting at their local sports team or local
newspaper frequently, but those accounts not appearing in the reference
dataset at all.

Once we switch to analysing topics rather than an individual's tweets, we
should probably add back in usernames. Being able to use the opposite
side's tweets as the reference dataset should balance out any local
accounts that might be tweeted at by both sides. If one side tweets to a
certain account a lot more than the other side, it would be worth seeing.

#### Stemming
We have an issue with stemming in that it is usually a one way process.
Information Retrevial systems don't care if the original word was "computer"
or "computes" as they're both considered "compute". The purpose of the word
cloud however is to display to humans what are the most common terms are.
Nonsense words like "exampl" just make it seem like there's something
glitchy with the system. If we want to use stemming, we must find a way
to recover the initial form of the word.

The initial solution I can think of is have a dictionary of key value pairs,
with the stemmed words as the keys and then a counter like object as the
corresponding value. The counter would count how often each term was stemmed
into the key. When we need to generate the word cloud, we look up each stem
and choose the most common original version. It doesn't seem overly efficent
however, either from a time or space perspective, so more work is needed in
the area.

I haven't implemented this solution because in the current architectural
design, the tweet parsing section and the word cloud generating section
should be spearate. This means an in memory solution like what's described
above wouldn't work. Some cache or persistance layer is needed in between
them, which will need to be designed with this system in mind. Until we
have this set up, there doesn't seem to be much point in implementing
stemming.
