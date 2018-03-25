# Pre-processing

Pre-processing is the initial manipulation of data into a format better suited to being fed into a machine learning algorithm. Just passing in raw text to a classifier would yield very poor performance, so it has to be prepared first. There are many Natural Language Processing (NLP) techniques that can be used to process data, some of the ones I used are:

* Case converting: This transforms all the Tweet's text to lower case, ensuring the classifier recognises `fun` and `Fun` as the same term.
* Tokenization: This involves splitting up a body of text into its component words (called tokens). A simple example of this is the sentence "I like eggs" becoming `["I", "like", "eggs"]`. There are a number of different tokenization strategies that yield different results, e.g. "I  didn't" could become `["I", "didn't"]` or `["I", "did", "n't"]`. The tokenizer I'm using is from the NLTK library and is optimised for high performance on Twitter data.
* Hashtag stripping: To allow the classifier to recognise that `fun` and `#fun` are the same term, we're stripping away any hash symbol that starts off a word. This is especially important for processing Twitter data, given the widespread use of hashtags on the platform.
* Removing unwanted terms: Certain words carry no informational value. Known as stop-words, they're very common and include terms such as "the", "as", "at", "on" etc. These can be stripped out in order to reduce the dimensionality of data sent to the classifier. Other terms that we're stripping out are links and Twitter usernames, as they would be of no use to the classifier.
* Stemming: This tries to reduce words to their root form. This allows the classifier to treat related words as the same value. E.g. "computational", "computer" and "computing" are all stemmed to "comput". There are many different algorithms used for stemming but I found the snowball stemming technique to perform best for my dataset.

Once a Tweet has been processed following the above steps, it is then ready to be sent to the classifier. It is modelled using a "bag of words" approach (also known as a vector-space model), in which the processed Tweet's terms are stored as an unordered list (i.e. multiset). It is quite a simple model that doesn't require any linguistic knowledge, yet generally performs quite well. It is widely used for text classification [1].

[1] - The Conversational Interface: Talking to Smart Devices by David Griol and Michael F. McTear
