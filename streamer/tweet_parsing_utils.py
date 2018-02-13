import re


class TweetParser(object):

    def __init__(self, config):
        self.hashtag1 = config["topic1"]["name"]
        self.hashtag2 = config["topic2"]["name"]
        self.languages = config["supportedLanguages"]
        self.timezones = config["supportedTimezones"]
        self.tracked_hts = {self.hashtag1, self.hashtag2}

    def get_tweet_viewpoint(self, status):
        text = TweetParser.get_tweet_text(status).lower()
        used_hts = re.findall("#\w+", text)
        # This regex is used to match hashtags, it means hash symbol followed by at least
        # one word character

        if len(self.tracked_hts.intersection(used_hts)) != 1:
            raise ValueError("Tweet contains wrong number of important hashtags")

        # At this point we know exactly one of the 2 hashtags were used,
        # so we can assume if it's not one, then it's the other
        return self.hashtag1 in used_hts

    def is_tweet_valid(self, status):
        if status.lang not in self.languages:
            return False
        if status.user.time_zone not in self.timezones:
            # if we know they're not in Ireland, should they get a say?
            return False

        try:
            self.get_tweet_viewpoint(status)
        except ValueError:
            # Tweet must have an illegal number of hashtags
            return False

        return True

    @staticmethod
    def get_tweet_text(status):
        try:
            tweet_text = TweetParser._get_status_text(status.retweeted_status)
        except AttributeError:
            tweet_text = TweetParser._get_status_text(status)

        return tweet_text

    @staticmethod
    def _get_status_text(tweet_status):
        try:
            return tweet_status.extended_tweet["full_text"]
        except AttributeError:
            # if it wasn't a long tweet, just get it the normal way
            return tweet_status.text
