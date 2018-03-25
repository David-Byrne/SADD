# Introduction

Sentiment Analysis is the field of computing associated with extracting emotions, attitudes or opinions from a body of text. It is currently one of the fastest growing research areas of computer science, mostly due to the popularity of social media. Common approaches include a combination of machine learning and/or natural language processing (NLP) techniques. Twitter, a microblogging based social media platform, is commonly used as a subject for sentiment analysis. This is likely due to a number reasons, including: it provides a well documented API, Tweets are public by default and the short character limits enforces succinctness.

The goal of the project is to use a combination of NLP and machine learning methodologies to conduct sentiment analysis on Twitter data. The system should be able to be applied to any topic and still yield valuable results. It should be capable of dealing with large volumes of data whilst still maintaining low latencies. Ideally it would be easily open to modifications such as adding extra data sources, different methods of analysis, alternative displays of results etc. Designing and implementing a system that can fulfil these requirements will result in many technical challenges. The rate of Tweets can dramatically spike without any warning, causing the system throughput to increase by orders of magnitude in a short period of time. This requires a highly scalable design to cope with sudden changes in input volume. Allowing for the potential addition of new features in the future requires a highly modular system design. Without this, it would turn into a highly complicated, monolithic system with a much higher chance of containing bugs and a much slower development rate.

Abortion has been a controversial political and social issue in the Republic of Ireland for many years. Despite it already being illegal under the Offences Against The Person Act, 1861, a referendum was held in 1973 to enshrine the right to life of the unborn in the constitution [1]. The proposed wording of the amendment was:
> “The State acknowledges the right to life of the unborn and, with due regard to the equal right to life of the mother, guarantees in its laws to respect, and, as far as practicable, by its laws to defend and vindicate that right.” [2]

Despite the attorney general at the time describing the wording of the amendment as "ambiguous and unsatisfactory", and stating that he could not "approve the wording of the proposed", no changes were made [3]. In what turned out to be an extremely controversial and divisive campaign, the referendum was passed with a 67% majority, despite the Taoiseach campaigning against it [4] [5]. It became the 8th amendment in the constitution, making Ireland the only democratic country in the world to have a constitutional ban on abortion [6]. A number of other referendums followed, to clarify the ambiguous ban on abortion. The most recent of these, the 25th amendment in 2002, looked to remove the threat of the mother's suicide as being legal grounds for abortion. This was rejected by a very slim majority of 50.42% [4].

This project's aim is to develop a machine learning based, sentiment analysis system, that can be used to analyse discussion of any divisive subject on Twitter. We will use the campaign to repeal the 8th amendment of the Irish constitution as a real-world test case to validate the system. It should be generic enough to allow it to be applied to any domain however. As Twitter is primarily used as a reactionary social network, this makes it ideal to analyse changes in sentiment as events unfold. Given how sensitive the topic of abortion is, as well as how divisive related referendums have been in the past, it is likely one of the best topics to test the system against.


[1] - [The Offences Against The Person Act, 1861](http://www.irishstatutebook.ie/eli/1861/act/100/enacted/en/print.html)

[2] - [Bhunreacht na hEireann](https://www.constitution.ie/Documents/Bhunreacht_na_hEireann_web.pdf)

[3] - [Peter Sutherland’s 1983 advice on the Eighth Amendment](https://www.irishtimes.com/news/social-affairs/peter-sutherland-s-1983-advice-on-the-eighth-amendment-1.3353263)

[4] - [Referendum Results 1937-2015](https://www.citizensassembly.ie/en/Manner-in-which-referenda-are-held/Referendum-Results-1937-2015.pdf)

[5] - [History lesson: What happened during the 1983 abortion referendum?](http://www.thejournal.ie/abortion-referendum-1983-what-happened-1225430-Dec2013/)

[6] - [Why Ireland became the only country in the democratic world to have a constitutional ban on abortion](https://www.irishtimes.com/news/politics/why-ireland-became-the-only-country-in-the-democratic-world-to-have-a-constitutional-ban-on-abortion-1.1907610)
