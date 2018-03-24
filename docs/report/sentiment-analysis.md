# Sentiment Analysis

Sentiment analysis is the process of determining the emotional tone of a piece of text. Its roots can be traced back to the studies on public opinion analysis at the beginning of the 20th century. Computational linguists became involved during the 1990's. The field rapidly grew in popularity with the rise of social media and 'Web 2.0', beginning in 2004. It is currently one of the fastest growing research areas in computer science [1]. Humans tend to only agree about 80% of the time on sentiment classification which demonstrates the difficulty of the problem [2]

It is widely used by large businesses and other organisations to analyse brand image and reveal customer insights. A number of companies specialise in social media sentiment analysis and sell their software as a service (SAAS), including BrandWatch and Hootsuite. These offer various features including sentiment trends per individual topic, demographic analysis, ranking common terms and alerting for sudden changes in sentiment. It has also been applied to try and predict changes in the stock market [3]. It is clearly an area with a high potential financial value, if applied correctly.

Politics is another area that sentiment analysis has been applied to. The Obama administration used sentiment analysis to gauge public opinion, especially among core supporters, to policy announcements during the 2012 US presidential campaign [4]. It has even been used to try and predict the results of elections in advance, although with mixed levels of success.

Andranik Tumasjan et al. found Twitter activity reflected the results of the German federal election in 2009. Using the Twitter Search API, they collected just over 100,000 Tweets referencing a political party or a leading politician in the month before the election. They analysed the Tweets with the Linguistic Inquiry and Word Count software (LIWC2007), a proprietary Natural Language Processing (NLP) tool. They found the number of Tweets about each party reflected voter preferences. Frequently co-occurring political parties in Tweets matched up to political ties and coalitions. They also found that the political sentiment expressed by Tweets closely corresponded to the political parties' positions [5].

The SSIX (Social Sentiment analysis financial IndeXes) project in collaboration with the Insight Centre for Data Analytics in NUI Galway monitored Twitter activity regarding the 'Brexit' referendum in the UK. Using the Twitter Streaming API, they collected around 10.5 million Tweets in the run up to, and aftermath of, the voting day. They trained a deep learning classifier using a manually annotated corpus, resulting in a model with an accuracy rate of 69%. Although the final result of the referendum was 51.9% 'leave', their models had 'remain' consistently on front. While the polls were open, the SSIX system analysed that 57.5% would vote stay, 9.4% off the actual figure of 48.1%. They concluded that although a large quantity of Tweets were collected, demographic, geographic and socio-economic differences between Twitter users and the UK electorate could have led to the bias in the predicted results [6].

There are two common styles of techniques used for sentiment analysis, lexicon-based approaches and machine learning approaches. Lexicon-based approaches include methods such a dictionary-based approach, where the text is checked against a known dictionary of positive and negative terms, and a corpus based approach, where statistical similarities are calculated between the text and a pre-existing corpus to determine the likelihood of the text being negative or positive. Machine learning approaches tend to involve training a classifier with some labelled data, to generate a model that can be used to classify previously unseen text [7].


[1] - [The Evolution of Sentiment Analysis - A Review of Research Topics, Venues, and Top Cited Papers](https://arxiv.org/pdf/1612.01556.pdf)

[2] - [How Companies Can Use Sentiment Analysis to Improve Their Business](https://mashable.com/2010/04/19/sentiment-analysis/)

[3] - [Twitter mood predicts the stock market](https://arxiv.org/pdf/1010.3003&)

[4] - [Obama’s Campaign Used Salesforce.com To Gauge Feelings of Core Voters](https://blogs.wsj.com/cio/2012/12/07/obamas-campaign-used-salesforce-com-to-gauge-feelings-of-core-voters/)

[5] - [Predicting Elections with Twitter: What 140 Characters Reveal about Political Sentiment](https://www.aaai.org/ocs/index.php/ICWSM/ICWSM10/paper/viewFile/1441/1852)

[6] - [In or Out? Real-Time Monitoring of BREXIT sentiment on Twitter](http://ceur-ws.org/Vol-1695/paper31.pdf)

[7] - [Sentiment analysis algorithms and applications: A survey](https://www.sciencedirect.com/science/article/pii/S2090447914000550)
