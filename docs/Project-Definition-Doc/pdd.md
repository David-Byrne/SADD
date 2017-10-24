# Real-Time Contrasting of Political Sentiment on Twitter

## Project Definition Document

***

## Project Description
> What we're doing

Ireland is set to hold a controversial referendum in the Summer of 2018 on
whether or not to repeal the 8th amendment. The 8th amendment of the Irish
Constitution acknowledges "the right to life of the unborn, with due regard
to the equal right to life of the mother" [1]. Effectively, this means a ban
on abortion in almost all circumstances. This has been criticised by various
international organisations including the United Nations who describe it as
"violating women's human rights" [2] and Amnesty International who claim it
puts "women's health at great risk" [3].

Many people use Twitter to share their opinions on topical events. This makes
Twitter a valuable source of data for sentiment analysis on current events as
people can see something and Tweet a reaction almost instantly.

This project involves taking the lead up to the 8th amendment referendum
as a case study on sentiment classification in a divisive domain and
displaying real-time sentiment scores for both sides. As an addition to the
sentiment analysis aspect, a word cloud will be created for each side
displaying the terms they use most relative to the other side.


## Purpose
> Why we're doing it

Obviously when dealing with a topic as sensitive as abortion, emotions are
high on both sides of the debate. Modern politics relies heavily on social
media to spread awareness and influence undecided voters. Both sides are
expected to campaign heavily all across social media. This should lead to
strong displays of sentiment from both sides of the debate. Twitter is an
ideal case study to measure this sentiment due to its real-time nature and
character limit that enforces conciseness.

Creating a word cloud of each side's relatively most used terms should also
give us an insight into what areas each side are focusing on. We'd hope to
see differences in the language used by both sides, and perhaps what type of
arguments they are using to try and convince undecided voters.

Being able to classify sentiment in real-time will hopefully give us great
insight into the nature of the campaign and how it changes over time. We'd
hope to see spikes in either positive or negative sentiment correlating with
important events in the lead up to the referendum. We'd also hope to see
what, if any, differences the two sides have on average sentiment over the
campaign and how it affects them.


## Problem/Opportunity
> Why it's worth doing as a project
> Maybe merge with above?

Although the vote itself will happen after the final submission is delivered,
the referendum campaign still gives us a great opportunity to analyse
sentiment in real-time for what looks to be one of the most controversial
votes Ireland has had in years.

Creating the system in the run up to the referendum will allow us to collect
far more Tweets than would be possible if we only started after the
referendum, as the normal Twitter Search API only allows you to query the
last 7 days worth of Tweets [4]. There is an enterprise level search but
that only allows querying of up to 30 days of historical data [5]. Both of
these searches focus on relevance rather than completeness meaning it would
be an incomplete dataset. Streaming the relevant Tweets from Twitter and
storing their IDs will allow us to build a dataset focused on this
referendum that's larger and more complete than anything that could be
generated after the campaign.

## Project Goal
> Ideally what we hope to achieve

The goal of the project is to create a system that can give us great insight
into sentiment on any controversial issue on Twitter. We will use the 8th
amendment as the initial proof of concept but the system will ideally be
able to switch domain with minimal changes needed.

We will investigate what strategies give us the best insights into the
sentiment of the population and also the differences in sentiment between
the two sides of the debate. Various machine learning and natural language
processing (NLP) techniques will be attempted.

The results of the real-time analysis and classification will be displayed
on a live updating website. This should be designed in a such a way that it
can be clearly understood by a general member of the population, allowing
them to gain an insight into the sentiment on Twitter from both sides of the
debate.

## Project Objectives
> Steps that will bring us to our goal

## Technologies
> Technologies used and why

## Project Timeline
> Overview of key milestones with their target date
> Gantt chart either here or at the end

## Project Scope
> What is and isn't included

## Assumptions and Constraints
> What it says on the tin really...

## References
[1] - https://www.taoiseach.gov.ie/DOT/eng/Historical_Information/The_Constitution/Constitution_of_Ireland_-_Bunreacht_na_h%C3%89ireann.html

[2] - https://www.irishtimes.com/news/health/irish-abortion-law-violated-woman-s-human-rights-un-says-1.3118145

[3] - https://www.amnesty.ie/abortion-faq/

[4] - https://developer.twitter.com/en/docs/tweets/search/overview/basic-search

[5] - https://developer.twitter.com/en/docs/tweets/search/overview/30-day-search

