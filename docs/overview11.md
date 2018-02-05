## Wordcloud Links
Clicking on any term in a wordcloud will now open a Twitter page containing
results for that specific term co-occuring with that viewpoint's hashtag.
For example, clicking on the term 'weaponised' in the #Repeal cloud opens
[these results](https://twitter.com/search?q=%23repealthe8th%20weaponised).
From this you can tell they're discussing people with down syndrome being
weaponised by the debate and being used as poster children. This should
give us a much better insight into the context of terms occurring in each
wordcloud.

## Benchmark IDF Corpus
As discovered last week, the NLTK's twitter dataset is unusually political
in nature as it was collected during the UK's 2015 general election. I've
changed to using NLTK's corpus of 'overheard conversations' instead. It
still uses very relaxed and colloquial language like that used on social
media, but it provides a much better representation of day to day word
usage.

## Docker
To focus on the development side of the project for a while, I got all the
microservices running as Docker containers. This means if anyone was trying
to get the pipeline running themselves, they wouldn't need to mess with all
the dependencies to get everything running. Simply having Docker installed
will allow you to satisfy every dependency automatically. Deploying the
pipleline will be as simple as cloning the repo and running `docker-compose
up`.

I'll keep the production server running everything natively as I've got it
all set up and I'm happy with systemd managing the processes. For
local development work and for people wanting to try out the system however,
the docker option is a much easier approach.
