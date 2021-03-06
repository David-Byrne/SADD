# Results

The primary goal of the project has been fulfilled. We have created a microservice based, machine learning pipeline, that can collect, classify and analyse Twitter data on any divisive domain and display these results in a web-based dashboard in real time. We have used the run up to the referendum on repealing the 8th amendment in Ireland as an initial, real-world test case to validate the system, and displayed the results in real-time on [hateful8th.com](http://hateful8th.com/).

## Raw Data
The pipeline has been running almost constantly since the 8th of November, 2017. Since then, it has collected over 250,000 Tweets regarding the 8th amendment debate. This makes it an extremely valuable corpus detailing the run up to one of the most important and controversial referenda in recent Irish history. It is my intention to keep the pipeline running until after the referendum is held, to increase the coverage of the dataset. Although this project will be finished by then, it would seem like a waste of a major opportunity to not keep the pipeline running until the end.

![daily_tweet_count](images/daily_tweet_count.png)
#### Figure 10.1: The number of Tweets collected daily since the pipeline began.

This graph is quite a simple visualisation of daily Tweet count. It does highlight many of the key events of the campaign so far, showing Twitter is being used to discuss news as it breaks. Some of the important events that have a noticeable impact on the graph include:
* 2017-11-18: Sinn Féin adopts a united party position to repeal the eighth amendment [20].
* 2017-12-13: Oireachtas committee votes to recommend repealing the eighth amendment [21].
* 2017-12-20: Oireachtas committee publishes final report, recommending a repeal of the 8th amendment [22].
* 2018-01-10: Taoiseach raises concern that allowing abortion up to 12 weeks may be a step too far [23].
* 2018-01-17: 8th amendment debate commences in the Dáil [24].
* 2018-01-26: First poll shows majority want to repeal the 8th amendment [25].
* 2018-01-29: Government formally decides to hold referendum. Taoiseach declares support for repealing the 8th amendment [26].
* 2018-02-10: An outage in the pipeline results in a number of hours of Tweets being missed.
* 2018-02-18: Regina Doherty TD says unless something is done, the referendum will not pass [27].
* 2018-02-21: Dáil debate on 8th referendum concludes [28].
* 2018-03-08: International Women's Day [29].
* 2018-03-10: 'Rally for life' held, where tens of thousands marched calling for the preservation of the Eighth Amendment [30].
* 2018-03-21: Dáil passes bill to allow the holding of a referendum on the Eighth Amendment [31].
* 2018-03-22: 'Together for Yes' campaign launched to advocate for a repeal of the Eighth Amendment [32].
* 2018-03-28: The date of the referendum is confirmed by the government [33].

![daily_tweet_count_by_viewpoint](images/daily_tweet_count_by_viewpoint.png)
#### Figure 10.2: The number of Tweets collected daily since the pipeline began, split by viewpoint.

Here we see the daily Tweet count, split into the distinct viewpoints. The most obvious piece of information from this graph is the difference in volume of Tweets from either side. #RepealThe8th is a much more common term than #SaveThe8th. This would be expected however as the main demographics on Twitter are more likely to be pro-choice [34] [35]. It is hard to make comparisons between the 2 activity levels, due to the large difference between them. To counteract this, I graphed the same data, but normalised it by the average Tweet count for that particular viewpoint.

![relative_daily_tweet_count_by_viewpoint](images/relative_daily_tweet_count_by_viewpoint.png)
#### Figure 10.3: The number of Tweets per day for each viewpoint, relative to the average number of daily Tweets for that viewpoint.

This gives us a far clearer comparison between the two viewpoints' activity levels. We can see there are certain news stories that are far more important for one side than the other. E.g. International women's day on March 8th was a much bigger event for the Repeal side than for the Save side. The 'Rally for Life' march 2 days later generated a much larger increase in Save activity than Repeal activity. It also shows up events that didn't produce a noticeable impact in the simple count graphs. E.g. A large spike in Save activity on March 29th, when the Save the 8th campaign officially launched [36]. There's no unusual spike in activity in the other graphs however as a decrease in Repeal activity masked the impact. Another clear feature of this graph is the increase in Twitter activity from both sides over time. The Save activity noticeably increased after the first poll showed Repeal with an early lead, on January 26th. As the referendum date gets nearer, we can expect to see further growth in activity levels from both sides.

## Tweet Time Analysis
What time people tend to Tweet about this debate at is another area to explore. As can be seen from above, large spikes in Twitter activity tend to follow big news breaking. I analysed the timestamps of all the Tweets the pipeline has classified to see if any interesting information could be extracted. Potentially, this sort of data could be used by groups to maximise exposure for Twitter campaigns on the topic.

![avg_tweet_count_by_hour](images/avg_tweet_count_by_hour.png)
#### Figure 10.4: The median number of Tweets per hour of the day.

I used the median number of Tweets as I felt using a mean average would result in outliers from large news stories distorting the true Tweet pattern. The graph looks quite like what you would expect. It's at its lowest at about 5 a.m., when most people would be asleep. It then climbs steadily from 6 a.m. until 10 a.m. when it plateaus. This corresponds to most of the population waking up and getting ready in the morning. The Tweet levels stay quite steady until after 4 p.m. There is a small spike at 5 p.m. which matches people finishing work and perhaps catching up on the day's activity on Twitter. It slumps a little from 6 p.m. until 8 p.m. which is when people would likely be getting dinner. There's then a larger spike in activity from 9 p.m. until 10 p.m. when people might be relaxing on social media at the end of the day. The Tweet levels then start to drop fairly  consistently until about 2 a.m., where they bottom out until about 6 a.m. The activity levels matching an average Irish person's day so closely also imply there's little foreign influence in the data. If the Tweet peak was at 4 a.m., that would be unexpected and probably a sign of something going wrong, as the activity would likely be coming from another part of the world that was mostly awake at that time. The lack of surprising results can be considered a good sign that our data is likely valid.

![avg_tweet_count_by_day_of_week](images/avg_tweet_count_by_day_of_week.png)
#### Figure 10.5: The median number of Tweets per day of the week.

Again, the median was calculated as very important days during the debate would be large outliers. Unlike the hour of the day graph, this one doesn't really have a shape that could be easily predicted. It would be hard to know in advance what days would be more active than others. Surprisingly, the most active day for Tweets on the topic was Wednesday. The middle of the week seemed to be the busiest portion with Wednesday, Thursday and Tuesday making up the top 3 most active days. The weekend and its surrounding days were much quieter overall. Potentially this could be explained by the majority of Twitter activity on the issue being reactionary. If TDs or campaigners aren't working at the weekends, there is less to react to which reduces activity. There could be a number of factors that are influencing this graph however.

## Sentiment

Analysing sentiment is the most challenging aspect of the project. Despite the classifier having an accuracy rate of slightly over 80%, which is marginally better than average human accuracy, it still results in almost 1 in 5 Tweets being mis-classified. This adds an extra layer of uncertainty which makes extracting information form the data more difficult. In order to reduce the noise in the calculated sentiment data, I calculated a weighted moving average for the sentiment on any given day. I felt this would be a fairer figure as many people wouldn't Tweet about the topic every day, but their sentiment towards it would be unlikely to change drastically in a short period of time. This smoothed the data, making any trends contained in the data easier to see.

![sentiment](images/sentiment.png)
#### Figure 10.6: The sentiment over the course of the debate so far.

This shows the smoothed sentiment calculated so far by the pipeline. It is displayed in the range [-1,1] as we found this to be a more user-friendly option than the usual range of [0,1]. For the remainder of this section, all figures for sentiment will be given for the [-1,1] range to keep consistency with the graph.

It can clearly be seen from this graph that the sentiment values were more extreme nearer the start of the debate, especially on the Save side. This is more likely to do with the lower levels of Twitter activity nearer the start, than any calming of discussion. As seen in the above subsections, there was very little Save Twitter activity in the first few months of measurements. This means noise had a far greater impact as a few extra negative Tweets in a day noticeably brought down the average. From mid-January onwards, almost all daily values have kept within the [-0.2,0.4] interval. This coincides with the increase in Twitter activity discussed above.

Unlike the above section on Tweet volumes, it is much harder to link any changes in the graph to specific events in the campaign. The rate of Tweets may increase but the overall sentiment doesn't swing outside of the usual fluctuation zone. The overall sentiment levels are too changeable to say with any confidence that a particular fluctuation was caused by a specific event. As the referendum draws nearer, it's possible that reactions to certain news stories would be more uniform, resulting in clearer changes in sentiment. An example of this would be on results day, where we would expect very positive Tweets from the winning side and potentially very negative Tweets from the other.

![mirror sentiment](images/mirror-sentiment.png)
#### Figure 10.7: Sentiment levels moving in the same directions.

![inverse sentiment](images/inverse-sentiment.png)
#### Figure 10.8: Sentiment levels moving in opposite directions.

Interestingly, a number of patterns are visible in the sentiment data between the 2 sides. For some short periods of time, both sentiment levels tend to change in a synchronised manner (fig. 10.7 above). They rise and fall on the same days, even when there's a large gap in their real values. A possible explanation for this is that sentiment expressed by one side is reacted to in a similar manner by the other side. A polite debate would likely result in positive sentiment from both sides, whereas an angry one would likely result in negative sentiment. Inversely, for other short periods of time, they move in opposite directions (fig. 10.8 above). This is probably closer to what one might expect, as positive news for one side would likely be negative news for the other (e.g. poll results showing one side has a large lead).

The overall average sentiment for Repeal Tweets is 0.1002 and for Save Tweets is 0.1968. Surprisingly, both values are positive meaning the debate might not be as negative as some feared it would be. It also shows Save supporters may be slightly more positive than Repeal supporters, although there is very little between the two sides.

## Word Clouds

Some of the most interesting findings from the pipeline have come from the word clouds. They were designed to show any differences in the language between the two sides, and also show what topics they were each most interested in at a given time. They only focus on recent discussion to get an idea of the trending topics, so they can be seen as a looking glass into the current status of the debate.


![wordclouds mar 11](images/wordclouds_2018-03-11.png)
#### Figure 10.9: The trending topics in the word clouds, on March 11th, 2018.

This image of the word clouds shows the different types of language used by both sides in the debate. Repeal, for example, frequently used terms including:
* magdalene laundries
* miscarriage
* ffa (Fatal Foetal Abnormalities)
* forced
* #TrustWomen

In general, these topics focus on the woman's rights and experiences. Save, on the other hand, uses terms including:
* innocent
* unborn
* killing
* #NoToTorture
* #SaveLives

Save seem to be using more emotive language focusing more on the unborn. Although this is only a single snapshot of the word clouds, the same style of arguments and terms re-appear regularly from their respective sides.

![wordcloud snow day](images/wordcloud-snowday.png)
#### Figure 10.10: The Repeal word cloud from March 2nd, when Ireland was suffering a massive snow storm.

Another strategy, used particularly by the Repeal side, that was highlighted by the word clouds was the linking of the debate to other news stories. The repeal word cloud, from when Ireland was suffering a large snowstorm on the 2nd of March, clearly shows this concept [37]. Many of the trending terms are to do with the weather, including:
* #snow
* #snowday
* #SneachtaForChoice (sneachta being the Irish word for snow)
* #BeastFromTheEast
* The 'snowflake emoji'

Initially looking at these, there's no clear relevance to the debate. After cross checking them on Twitter however, a narrative became clear. People were Tweeting about the women who'd be trying fly to the UK for an abortion, but who were prevented travelling due to flights being cancelled. By linking their agenda to the most popular news story, they were hoping to get focus back to their arguments.

![wordcloud march](images/wordcloud-march.png)
#### Figure 10.11: The Save word cloud from February 26th, when they were promoting a rally.

Dates and times for events are commonly very popular terms in the word clouds, since they are likely only related to one side. An example is this Save cloud, where we can see the key details of the "All-Ireland Rally for Life". This was taking place on Saturday the 10th of March, from 2pm in Parnell square, and was organised by Youth Defence [38].

![Twitter Lookup](images/twitter-search.png)
#### Figure 10.12: Twitter search results that are automatically opened when clicking on a term in a word cloud. In this case the results shown correspond to clicking on the '#BeastFromTheEast' term in the Repeal word cloud.

Clicking on a term in a word cloud opens Twitter search results for the corresponding Tweets in a new tab. It does this by dynamically building a Twitter query string containing the selected term, as well as the main term in the word cloud to add context. As can be seen in the above image, it clarifies terms that on their own don't seem to have much relevance to the debate. This feature has been very useful to fill in the context missing from the word clouds.

## Configurable Pipeline
Although all the above results are specific to the 8th amendment referendum debate, the core pipeline is entirely configurable. To demonstrate this, I modified the config.json file that determines the target topic and didn't touch anything else. I then re-deployed the pipeline and collected a small set of new results. The new topic I chose was the battle between 2 highly popular gaming consoles in America, the Nintendo Switch and the PlayStation 4. The modified config.json file is as follows:
```` json
{
    "topic1": {
        "name": "#NintendoSwitch",
        "colour": "#e80113"
    },
    "topic2": {
        "name": "#PS4",
        "colour": "#06418d"
    },
    "name": "Console Wars",
    "tagline": "Real time Gaming Console analysis on Twitter",
    "supportedLanguages": ["en"],
    "supportedTimezones": ["Eastern Time (US & Canada)", "Central Time (US & Canada)",
        "Mountain Time (US & Canada)", "Pacific Time (US & Canada)"]
}
````
This specifies all the details that are specific to the topic being analysed. As can be seen from the configuration file, the pipeline was set up to analyse Tweets containing either #NintendoSwitch or #PS4 from North America in English. After running the pipeline for a few hours over 3 consecutive days, this is what the results page looked like:

![Nintendo Switch vs PlayStation 4](images/switch-vs-ps4.png)
#### Figure 10.13: This shows the web frontend of the pipeline after collecting data on gaming console discussion from North America intermittently over the course of 3 consecutive days.

With only a few hours of data collected overall, it's clearly not enough to draw any results from. It does show however, that the pipeline can be pointed at another target and work perfectly.

## Real-world Release
Once I was happy that the development side of the project was complete, I posted a link to the website on the Irish forum of the social media site Reddit. I chose Reddit as it has a large focus on posting a topic and discussing it for a short while, before newer posts appear and the discussion shifts to them. This would allow me to demonstrate the website to a large amount of users without needing to have a large social network to share it with, as would be required on Facebook or Twitter. I set up Google Analytics to gather information on any web traffic I received. This, combined with the feedback given directly by Reddit users, would give valuable insight into real-world usage and value of the system.

The website received over 600 page views in the 24 hours after posting it on Reddit, according to the Google Analytics data. This figure underestimates the actual value, as many people run adblocking software which would also block Google Analytics from running. Of these recorded hits, 84.6% originated from Ireland, 5.1% from the United Kingdom and 2.5% from the United States. Given it was posted to an Irish forum, there's nothing overly surprising in these figures. 54% of users were on mobile phones, 39.5% on laptops or desktops and 6.5% on tablets. This statistic clearly shows the value that was added by making the site mobile friendly. Looking at the referral data, the vast majority of traffic came to the website via Reddit, which is what we'd expect. Interestingly though, there were small amounts of referrals from Twitter, Facebook and Messenger as well. This implies users on Reddit saw the link and further shared it to other people. In terms of users' systems, there weren't any surprising results with Chrome and Android Webview being the 2 most popular browsers and Android and Windows being the 2 most popular operating systems. English was by far the most popular language, with all but 2 users having it set as their main language. The remaining 2 users both had Irish set instead.

The general reception to the website on Reddit was extremely positive, with the post being 88% 'up-voted'. Many of the comments were by users who were impressed by the site, including:
> Wow. Very impressed OP. Well done. Absolutely love the name, very clever. I think you're onto a winner here. Start sharing it with news organizations.

> This is pretty cool

> I hope you dont mind but I tweeted out a link to the website and gave your reddit username. I've been fairly active on Twitter with the referendum so I think the website will benefit a lot of accounts

> Well done, this is an excellent project

> LOVE the name btw!


A number of users were interested in the technical inner workings of the system, which I found somewhat surprising. Science, Technology, Engineering and Maths (STEM) fields are highly represented on Reddit which could explain the unusual levels of interest.

> What algorithms did you use to determine the sentiment of the tweets?

> Is it up on github to take a nosey?

One user in particular was impressed enough to offer me a job based solely off the Reddit post.

> Wow. Very impressed. PM me if you're interested in some work.
