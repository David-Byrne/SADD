# User Feedback
In an attempt to further improve the user experience (UX) of the frontend of the system, a user feedback process was created. I created a feedback form based off the Questionnaire for User Interface Satisfaction (QUIS), which was originally developed by the University of Maryland [1]. I re-worded certain questions to make them more suitable for this application and I removed others which I felt were irrelevant. I tried to keep the questionnaire as minimal as possible to encourage more people to complete it, whilst still having a sufficient range of questions to generate valuable information.

The feedback form was created using Google Forms and then circulated using a shareable link. I tried to get a wide cross section of potential users, aiming for diversity in age, gender and computer literacy. The feedback form is completely anonymous however so there was no way for me to link answers to demographics. I felt this was the fairest approach as the small sample size may lead to the demographic information being potentially personally identifiable.

The feedback form began with a link to the web frontend and a disclaimer encouraging people to skip any questions they felt uncomfortable answering. It was then split into a number of sections, each comprising of a number of questions focusing on a certain part of the software. There were 12 responses submitted. The questions, as well as their answers are as follows:
* Overall reaction to the software
  * How good was the software?
    * This was marked on a scale of 0-9 with 0 labelled as terrible and 9 labelled as wonderful.
    * The average score was 7.27.
  * How easy to use was the software?
    * This was marked on a scale of 0-9 with 0 labelled as difficult and 9 labelled as easy.
    * The average score was 7.64.
  * How interesting was the software?
    * This was marked on a scale of 0-9 with 0 labelled as dull and 9 labelled as stimulating.
    * The average score was 7.73.
* Screen
  * Reading characters on the screen.
    * This was marked on a scale of 0-9 with 0 labelled as hard and 9 labelled as easy.
    * The average score was 7.42.
  * Organisation of information.
    * This was marked on a scale of 0-9 with 0 labelled as confusing and 9 labelled as clear.
    * The average score was 7.
* Terminology and System Information.
  * Use of terms throughout the system.
    * This was marked on a scale of 0-9 with 0 labelled as inconsistent and 9 labelled as consistent.
    * The average score was 8.25.
  * Computer informs about its progress.
    * This was marked on a scale of 0-9 with 0 labelled as never and 9 labelled as always.
    * The average score was 7.64.
* Learning
  * Learning to operate the system.
    * This was marked on a scale of 0-9 with 0 labelled as difficult and 9 labelled as easy.
    * The average score was 7.10.
  * Exploring new features by trial and error.
    * This was marked on a scale of 0-9 with 0 labelled as difficult and 9 labelled as easy.
    * The average score was 7.27.
  * Supplemental reference materials.
    * This was marked on a scale of 0-9 with 0 labelled as confusing and 9 labelled as clear.
    * The average score was 6.36.
* System capabilities
  * System speed.
    * This was marked on a scale of 0-9 with 0 labelled as too slow and 9 labelled as fast enough.
    * The average score was 8.72.
  * System reliability.
    * This was marked on a scale of 0-9 with 0 labelled as unreliable and 9 labelled as reliable.
    * The average score was 8.27.
  * Designed for all levels of users.
    * This was marked on a scale of 0-9 with 0 labelled as never and 9 labelled as always.
    * The average score was 6.91.
* General feedback
  * List the most negative aspects of the system.
    * This was entered as free form text.
    * A selection of answers are discussed later.
  * List the most positive aspects of the system.
    * This was entered as free form text.
    * A selection of answers are discussed later.

For the most negative aspects of the system, responses included:
> Would like to see that if I click on a particularly negative/positive day I could see what was trending then.

This was a common request and was actually thought up at one of the meetings with my supervisor. At that point though, we had already deleted the text from the majority of the Tweets we had collected up to that point. This would mean only part of the graph would let you see the trending terms. With the Tweet IDs we store permanently it would have been possible to recover the text from the Tweets. We decided in the end that it would have been too messy to implement this half way through the project, but it is something I would like to add before using the pipeline for another topic.

> See that it's showing a graph of sentiment over time...but what should I do with that information? Can I interact with it? Can I change parameters? Etc. How to use the system is unclear.

Another common piece of feedback was the desire to interact more with the system to drill down into the data. It was never designed with complex interactivity in mind however, more to act as a simple dashboard or looking glass into the data. If this was something we wanted to add in the future, taking advantage of a specialised data visualisation tool such as Kibana or Grafana would be a better approach. These would be far too complex for the simple overview we planned to provide for this project however.

> Although black and pink are very aesthetically pleasing, I would be wary of using them for something like this project as they may portray different connotations i.e. black traditionally meaning death, pink being love, etc.

Colour connotations was something I tried keep in mind when selecting colours for both sides. I ended up going with colours that are often used by each viewpoint, to associate each visualisation with the corresponding viewpoint, and also to avoid adding any potential bias from choosing colours myself. The colours I went for were black (like the "REPEAL" jumpers) and pink (like the "Love Both" advertising). They also offer sufficient contrast against the white background and text, as well as against each other for anyone suffering from colour blindness. This is an important factor to keep in mind from an accessibility point of view.

For the most positive aspects of the system, responses included:
> The minimalist design is awesome. The word-cloud is also amazing. Well done!

The overall design and UI was specifically complemented in a majority of responses.

> The words in the wordclouds linking back to Twitter made it very easy to understand the context of any word.

The linking of terms in the word clouds to Twitter was another popular feature. It clearly yielded a lot of benefit for quite a simple addition.

Overall the results were quite positive. Although it was not a large sample size of potential users, it was still very beneficial to receive feedback.

[1] - [Development of an instrument measuring user satisfaction of the human-computer interface](http://delivery.acm.org/10.1145/60000/57203/p213-chin.pdf) by John P. Chin, Virginia A. Diehl and Kent L. Norman (1988)
