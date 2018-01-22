# WordClouds
The big focus this week was getting the word clouds displaying real data. Up
until this point we were never storing the actual text of the tweet, just
some of its attributes. This had to change however as the word clouds need
to access the text. Rather than adding in another column into the main
sentiment table, I created a second table specifically for the tweet's text.
This meant I could treat them independently and so I'm able to delete any
tweets which I don't need any more without affecting the sentiment data. I'm
only storing the 500 most recent tweets of each viewpoint and creating a
word cloud from these.

To calculate the words and their weightings for the word cloud, I've started
off using a simple TF-IDF style approach. Each word is given a score equal
to the number of times it occurs in that viewpoint, divided by the number of
times it occurs in the opposing viewpoint plus 1. I've set the two sides
against each other like this to try see the difference in language the two
sides are using.

Then to display the data, I'm using logarithmic scaling of the word scores
to calculate their size. Without this the most frequent terms would be far
too big (eg #RepealThe8th). I've played around with the scaling factors a
bit to get it looking a bit better but they could probably do with a bit
more tuning at a later stage.

## Results
Results are mixed overall, it's a good initial proof of concept but
definitely needs some extra word in places.

#### Good
* I'm getting relevant terms to the debate. Eg Repeal cloud contains
: #repealthe8th, #namethedeputy, disability, @freesafelegal ... whereas
the Save cloud contains : #savelives, #resignnow, #irelandisprolife,
michéal ...

#### Not so good
* #SaveThe8th is missing... It should be in every Save tweet and it
shouldn't be in any Repeal tweets which should mean it'd have a very high
score, but it doesn't... It's not in the top 100 Save terms. #RepealThe8th
is by far the top of the Repeal cloud, as is expected, so I'm not sure
what's happening to #SaveThe8th...
* The links are all broken. Now it's possible they're all referring to
things that have since been deleted but that seems a little unlikely. I
could look into it more, but I'm not sure links belong in a word cloud at
all really so I might just remove them.
* Some words are there but they don't tell us much, eg cannot, there's,
let's, lot, 2, 3...

## ToDo
* Remove grammar - Commas, periods, question marks, colons are adding noise
to the data and should be removed
* Remove links - They don't add much value and seem to all 404 for some
reason
* Reduce repainting - Since the word cloud library I'm using doesn't support
updating a cloud, it means we've to re-paint it every time the data changes.
This happens every time the analyser runs which isn't ideal. It might be
better to check if there would be any big changes first before re-painting.
* Use more tweets? - If we went up to 1000 for each viewpoint it would mean
we're less susceptible to noise from a popular re-tweet, but it would also
show individual news stories less. There's a trade-off to be made somewhere.
* Maybe look into weighting differently?  TF^2/DF would reward terms that
appear more frequently, even if they also appear more frequently in the
opposing viewpoint as well.
