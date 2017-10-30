## PDD
This week began with a focus on the Project Definition Document. While not
the most exciting piece of work, it's good to have most of it out of the way.
Currently it's in draft format in markdown with the necessary images
generated. All that's left for next week will be to get the final 'ok' on
content and then format it into a proper doc.

## Naming
> "A rose by any other name would smell as sweet" - W. Shakespeare

Nevertheless, it's probably time some thought went into thinking about names
for the project. Ideally a name should be short, snappy and represent what
the project is about. Given the overall system should be able to be applied
to any controversial or divisive domain, we should avoid choosing a name that
focuses exclusively on the 8th amendment referendum debate. If I'm making a
website that focuses specifically on analysis of the 8th debate however, an
8th focused name would make sense in that case. The solution I'm leaning
towards at the moment involves 2 names, 1 for the system (generic) and one
for site focusing on the 8th (more specific, domain name available...).

* For the system name I've gone through many ideas but my current favourite
is: SADD - Sentiment Analysis in Divisive Domains. It's short, snappy, the
acronym makes sense, and thanks to [Donald Trump's tweeting habits](http://knowyourmeme.com/memes/donald-trump-s-sad-tweets)
, is a subtle nod to politics and twitter as well. It is used by some student
organisation in the states but I'm not concerned about that at all.

* For the site name, I'm currently favouring 'The Hateful 8th' - a play on
Quentin Tarantino's film title 'The Hateful 8". I've bought [hateful8th.com](https://whois.icann.org/en/lookup?name=hateful8th.com)
for now but we can always change to a different domain if needed later. The
only issue for this name would be SEO clashing with the much more famous
film but it's not a major worry since this is just a research project.

## Classification Microservice
This week also focused on the setting up of the classification microservice.
A lot of the important work had been done with the proof of concept
classifier which made this much easier. I have a script to train a model
based on the NTLK's Twitter corpus and then export it to a pickle file. The
classification service is a simple flask app that reads in model and uses
that to classify tweets as they are submitted to it. Using
[gunicorn](http://gunicorn.org/) to run the server allows us to take
advantage of multiple processes and much higher performance than the flask
development server offers.

Parallelising the classification microservice showed up a flaw in the
streaming service. We would wait to hear back from the POST request before
reading the next tweet from Twitter's stream. Obviously this is a problem as
it is a massive performance bottleneck, given classifying a Tweet could take
a non-trivial length of time and we were blocking every time a Tweet came
through. By including a thread-pool to handle sending the POST requests I've
worked around this issue allowing proper parallelisation of the pipeline.
