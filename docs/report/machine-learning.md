# Machine Learning

Machine learning is the field of computer science that allows computers to 'learn' how to perform a task without being explicitly programmed for that task. The computer can progressively improve performance at this task with experience (i.e. with sufficient training instances or attempts at the task). The two main branches of machine learning are supervised and unsupervised. Supervised machine learning can be thought of in terms of giving the computer examples of correct answers when it's being trained. An example of this is the classification task in the classifier service. We have Tweets that are marked (classified as) positive and Tweets that are marked (classified as) negative. These are given to the classifier and it learns a model from them to be able to classify Tweets it hasn't yet seen. Unsupervised machine learning doesn't have a training phase, it 'learns' the task as it goes. An example of this is how Google News groups different articles on the same story together. It finds similarities in the data on its own, then groups the articles into clusters based on the similarity. There may be a manually clustered "gold standard" to compare against, i.e., to check performance, but this isn't used to train the model.

The classifier service uses a form of supervised machine learning called classification. In this, the algorithm is fed in some data points with corresponding classes (i.e., the training data). It uses this data to learn a model on how best to predict the correct class, given only an unlabelled data point. There are a finite number of classes and they are all known beforehand. In our case, we only have two classes to identify (positive sentiment and negative sentiment) so we need a binary classifier.

To translate the Tweet text into a format a classifier can understand, I'm using a "bag of words" approach. This involves splitting each Tweet up into its terms, and then representing it as a vector of counts of every term in the dataset. As can be expected, these will be mostly 0 since most Tweets only contain a small subset of the overall collection of words.

To test the performance of a classifier, it's best practice to separate the dataset out at the start. A validation portion of the dataset should immediately be removed from the available training data and locked away, until the very end. This is used to give us an unbiased estimate of real-world performance since it's not involved in the model generation process at all. The remaining data can then be split into a training set (used to train the model) and a test set (used to check the model's accuracy). It's important not to mix these or else we would end up in a situation where we're testing the classifier on data it has already seen. This would be similar to students learning off an exam paper instead of studying the entire subject. As can be imagined, this would yield very biased and inaccurate results. We keep tweaking the model with the aim of maximising the performance on the test set. Rather than creating a training set and a test set however, I'm applying a process called "Cross Validation" in order to test the data. This entails splitting the dataset (after removing the validation dataset) into N layers. We run the training and test process N times, where in each case we select a different layer as the test set, train a model on the other N-1 layers and then assess its performance using the test set layer. After, we calculate the mean of the accuracy scores for each of the N models and this is determined to be the classifier's estimated accuracy. I'm calculating the accuracy to +/- 2 standard deviations to give a good performance range. Given there are only 2 classes, a random guessing algorithm should have an accuracy of 50%. This is the baseline figure and anything above it is evidence that the model has learned from the data. [16]

There are a number of different classification algorithms, however no single one is guaranteed to be best for every problem domain. While it would be infeasible to try every algorithm and test its performance, testing the most popular algorithms should give good coverage of the main options. Scikit-learn, a Python machine learning library, has implementations of all of these. This allowed me to quickly test the various classification algorithms to find which style suited my problem domain the best.

An overview of the algorithms I tested out and their results are as follows:

* **Decision Tree**: This works by recursively building a tree, where each node is a "question" (decision point) about the number of occurrences of a certain term in the Tweet. This term is chosen at each point to maximise the reduction in uncertainty in the child datasets. The leaf nodes are classes. To classify a new Tweet, it starts at the root node and works its way downwards through the tree by answering the question at each node and choosing the appropriate child node to follow. When it arrives at a leaf node, it predicts that is the class the Tweet belongs to. Training this classifier against my data resulted in an accuracy of 76.01%, +/- 2.32%.

* **K-Nearest-Neighbour**: This classifier plots every training instance in an N-dimensional space, where N is the number of attributes each instance has. The instance's value at each dimension is the number of times the term corresponding to that dimension occurs. To classify a new instance, it plots it in the same multi-dimensional space. It then finds the N nearest instances and the majority class amongst them is predicted for the new instance. Letting N = 5 seemed to result in optimal results, with an accuracy of 72.96%, +/- 3.22%.

* **Logistic Regression**: This works by generating a sigmoid function that takes the attributes of an instance as an input and returns the probability of it being a member of a certain class as an output. It is a binary classifier as it relies on Boolean logic to specify an output. An example could be a sigmoid function that takes in a person's height and weight and returns the probability they're a male. An instance with weight 50 and height 160 might cause the function to return 0.05, which means there's a 5% chance they're a male. This would cause the classifier to predict the instance is a female. Training this classifier against my data resulted in an accuracy of 80.99%, +/- 1.98%.

* **Support Vector Classification**: This maps every training instance to an N-dimensional space, where N is the number of attributes each instance has, such that the gap between the classes is as wide as possible. It then stores the line in the centre of the gap and uses that as the divider between the classes. There are various methods (called 'kernels') to calculate the best gap so I tested a couple of them. Using an SVC classifier with a radial basis function (RBF) kernel resulted in an accuracy of 62.87%, +/- 2.73%. An SVC with a linear kernel (LinearSVC) got an accuracy of 79.71%, +/- 2.03%. An SVC with a sigmoid kernel scored an accuracy of 62.87%, +/- 2.73%.

* **Neural Network**: This uses a multi-layer perceptron (MLP) that has an input layer containing N nodes, a number of hidden layers and an output layer made up of a single node. Each of the input nodes correspond to an attribute of the data. Each layer's nodes are connected to some of the nodes in the next layer. Each node has a weighting that if a certain number of input nodes fire, it fires to every node it's connected to in the next layer. If the final output node fires it's a certain class, if not it's the other class. The connections and weighting for the nodes is learned during the training to optimise the accuracy. This classifier built a model with an accuracy of 76.47%, +/- 2.45%.

* **Bernoulli Naive Bayes**: This is a probability-based classifier that is based around Bayes' rule. It works out the probability the Tweet is a certain class by multiplying out the probabilities it contains each word given it's that class, by the probability of that class occurring. Training this classifier against the data built a model with an accuracy of 80.54%, +/- 2.06%.

* **Multinomial Naive Bayes**: Like the Bernoulli Naive Bayes, this is also based around Bayes' rule, except it takes word count into consideration when calculating probabilities. The vector used for input contains counts for each word, as opposed to Booleans for each word existing in the Tweet. Setting the internal weighting parameter alpha to 1.375 yielded a model with an accuracy of 80.16%, +/- 2.64%. [17]

Judging from these results, the top 3 algorithms best suited for this task are:
1. Logistic Regression @ 80.99%
2. Bernoulli Naive Bayes @ 80.54%
3. Multinomial Naive Bayes @ 80.16%

However, recall from the above that the fairest way to estimate real-world performance is to hide away a random selection of the labelled dataset at the very start. I locked away 1000 tweets (500 from each viewpoint) that I didn't use at all while developing or tuning the algorithms, since that could lead to a bias in the results. After building and optimising the models with the training sets, and being happy with the results, it was time to bring back the validation set. Testing the classifiers we've built against this dataset should give us a good estimate of real-world performance. I ran each of the top 3 algorithms as decided above against the validation set and the results were as follows:

1. Logistic Regression: 797 classified correctly, which gives an accuracy score of 79.7%. This is slightly lower than the training accuracy however it is still within the margin of error.
2. Bernoulli Naive Bayes: 803 classified correctly, giving an accuracy score of 80.3%. This is marginally lower than the training accuracy, however it's still well within the margin of error.
3. Multinomial Naive Bayes: 810 classified correctly, giving an accuracy score of 81.0%. This is actually higher than the training accuracy, but again well within the margin of error.

Interestingly, the top 3 algorithms in training accuracy scores have been reversed when testing against the validation set. Given these surprising results, I also tested the SVC with a linear kernel against the validation set, as it had quite close an accuracy rate to the top 3 algorithms in the training phase.

4. Linear SVC: 781 classified correctly, giving an accuracy score of 78.1%. This is lower than the training accuracy, although within the margin of error. It's also significantly lower than the other algorithms tested against the validation dataset.

Given that all the other algorithms have accuracy rates below the current leader, even when taking the upper bound from the margin of error, I decided there was no point testing them against the validation dataset. Although the top 3 algorithms all had similar performance levels, I decided to go with the Multinomial Naive Bayes classifier as it had the highest score against the validation dataset. This is the closest estimate to real
-world performance so I felt it was the fairest metric to judge it off.

While the validation dataset accuracy score gives a good estimate of likely real-world accuracy levels, it's also important to check the classifier's accuracy rate for each specific class. An example of this would be for a classifier that's used to detect a serious disease. It's much worse if it tells a sick person they're healthy (false negative) than if it tells a healthy person they're sick (false positive). Just using an overall accuracy figure hides this important performance statistic. For the classifier service, a general balance between the false negative and false positive rate would be ideal. This would mean the error rate is fairly spread between both classes. Even with an 81% accuracy rate, it's possible that it classifies nearly 40% of positive Tweets as negative, assuming it could correctly classify every negative Tweet. This would lead to a large bias in results, reducing their value. The accuracy on a class by class basis can be displayed using a confusion matrix. This is a table with the rows containing the actual classes, the columns containing the predicted classes, and the cells containing the number of results matching that combination. An example confusion matrix for a binary classifier is:
````
             |   P   P  |
             |   r   r  |
             |   e   e  |
             |   d   d  |
             |          |
             |   T   F  |
             |   r   a  |
             |   u   l  |
             |   e   s  |
             |       e  |
-------------+----------+
Actual True  |<TP>   FN |
Actual False | FP   <TN>|
-------------+----------+
````
Where
* TP = True Positive
* FN = False Negative
* FP = False Positive
* TN = True Negative

I generated a confusion matrix based on the 1000 Tweets in the validation dataset using the classifier built with the Multinomial Naive Bayes algorithm:
````
         |   n   p |
         |   e   o |
         |   g   s |
         |   a   i |
         |   t   t |
         |   i   i |
         |   v   v |
         |   e   e |
---------+---------+
negative |<403> 97 |
positive | 93 <407>|
---------+---------+
(row = reference; col = test)
````

This shows the accuracy rates for both classes are very close, with the classifier correctly predicting 80.6% of negative Tweets and 81.4% of positive Tweets. 4 Tweets in the difference is negligible given a sample size of 1000 Tweets. This means there shouldn't be a bias in the results generated by the classifier which is what we wanted to see.

The importance of the validation set can clearly be seen from the data above. It's also very important to detect over-fitting, which is when a model just learns the specifics of the dataset rather than the general techniques that are transferable across datasets. It doesn't seem to have occurred in any of the models tested above, but it's easily recognisable by a high score in the training accuracy but then a much lower score when being tested against the validation set. Without this extra check, it's possible to naively assume a good accuracy during the training phase corresponds to a good accuracy in real-world conditions, which isn't guaranteed.
