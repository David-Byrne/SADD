# Multinomial Naive Bayes

As this is the classification algorithm used by the classifier service, it's worth explaining it in a bit more detail with the help of a worked example.

We'll use a trivial example where we want to classify the sentiment of the Tweet "I like chocolate". In mathematical notation, we are trying to calculate `P(positive | I like chocolate)`. As the Naive Bayes family of classification algorithms are probabilistic classifiers, they return the probability of an input being a member of a certain class.

We need to train our classifier with a labelled dataset. In this example, we will use 3 Tweets from both classes:
* Positive Tweets:
  * Hot chocolate makes me happy
  * My kittens like me
  * Mom will like her birthday
* Negative Tweets:
  * I hate everyone
  * This music is like people screaming
  * Mondays are horrible

To prepare these Tweets, stop words are removed and frequencies are counted for each word for each class. Generally other pre-processing techniques are also applied, however they're skipped here for simplicity.

| Positive words| Frequencies |
|---------------| ----------- |
| hot           | 1           |
| chocolate     | 1           |
| makes         | 1           |
| happy         | 1           |
| like          | 2           |
| kittens       | 1           |
| mom           | 1           |
| birthday      | 1           |
| surprise      | 1           |

| Negative words| Frequencies |
|---------------| ----------- |
| hate          | 1           |
| everyone      | 1           |
| music         | 1           |
| like          | 1           |
| people        | 1           |
| screaming     | 1           |
| mondays       | 1           |
| horrible      | 1           |

We can now introduce Bayes' Rule which states `P(A|B) = [P(B|A) x P(A)]/P(B)`. In our example, this leads to the equations `P(positive | like chocolate) = [P(like chocolate | positive) x P(positive)]/P(like chocolate)` and `P(negative | like chocolate) = [P(like chocolate | negative) x P(negative)]/P(like chocolate)`. Since both equations are divided by a common term, `P(like chocolate)`, we can discard it for now and normalise the values later. We can now compare `P(like chocolate | positive) x P(positive)` against `P(like chocolate | negative) x P(negative)` and see which is larger.

We are very unlikely to be able to calculate the true probability of `P(tweet | class)` as it would require the exact Tweet to be in our training set or else we would give probability 0. To combat this, we can naively assume that each of the words (features) are independent. This allows us to say in our example that `P(like chocolate | positive) = P(like | positive) x P(chocolate | positive)`, and similarly for the negative sentiment class calculations.

The only potential issue with the above approach is if a Tweet contained a term that wasn't seen in the training set. This would lead to the probability calculations for each class returning 0 resulting in an inconclusive tie, even if every other term in the Tweet was strongly associated with one of the classes. To combat this, we introduce a technique called Laplace Smoothing. This involves adding an extra pseudo-instance to both classes that contains 1 of every possible attribute. This can be thought of as a Tweet that contains every word in our dictionary. Without smoothing, `P(hot | positive) = 1/10` as there are 10 terms in the positive dataset and hot appears once. With smoothing, `P(hot | positive) = 1+1/10+16` as the term hot now appears twice (once in an actual Tweet and once in the pseudo-instance) and the 16 distinct terms from the training set all appear in the pseudo-instance as well as the 10 terms normally occurring in the positive dataset.

We are now able to begin the calculations.
* `P(like | positive) = 2+1/10+16`
* `P(chocolate | positive) = 1+1/10+16`
* `P(like | negative) = 1+1/8+16`
* `P(chocolate | negative) = 0+1/8+16`

Given we have 3 Tweets from each class, `P(positive) == P(negative) == 3/6`

Now to fill in the equations from above:
* `P(positive | like chocolate) = 3/26 x 2/26 x 3/6 = 0.004438`
* `P(negative | like chocolate) = 2/24 x 1/24 x 3/6 = 0.001736`

As `P(positive | like chocolate) > P(negative | like chocolate)`, we can classify this Tweet as being positive.

To calculate exact probabilities, we have to normalise the figures since we discarded some of the equation earlier on the in calculations. I.e. the true probability of each class is the calculated probability of that class divided by the sum of the calculated probabilities.
* `TrueProb(positive | like chocolate) = 0.004438/ (0.004438 + 0.001736)`
* `TrueProb(negative | like chocolate) = 0.001736/ (0.004438 + 0.001736)`

This finally allows us to assign probabilities to our classification. We can say we're 71.88% sure "I like chocolate" is a positive Tweet and 28.12% sure it's a negative Tweet.

Obviously this example is an extremely trivial one, but it still shows the operations of a Multinomial Naive Bayes classifier.
