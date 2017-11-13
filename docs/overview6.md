## Hashtags
Cleaning up some issues that were noticed earlier but never addressed, I
re-did how hashtags are dealt with. Now we check if it contains a relevant
hashtag (occasionally Twitter sends up some that don't) and not more than
one (since I'm not sure how to handle a Tweet containing both '#savethe8th'
and '#repealthe8th'). If it doesn't satisfy both of these criteria, we drop
it.


## Server
We deployed the pipeline to a proper server this week for the first time, up
til now it was just run in short bursts on my laptop. We added systemd
support to monitor each of the services and restart them automatically if
they crash out. This has shown up a few potential issues (more later) but
it's mostly working smoothly.

As of Monday November 13th at 2 o'clock, we have collected 1274 tweets. The
aim is to leave it running for the foreseeable future as a larger dataset
is more valuable than a smaller one. Even if we decide to change how the
sentiment classification is handled, we have all the Tweet IDs so they can
all be re-processed without much hassle.


## SQL errors
Reading through the service logs, occasionally an SQL exception is thrown in
the classifier microservice, meaning the Tweet probably isn't inserted
correctly. There's no detail in the stack trace so I've added in a patch to
catch any SQL exceptions and log the details. It doesn't seem to be
happening frequently enough to need any urgent work, I'll keep an eye on the
logs for now to see if I can gain any more insights into the issue.
