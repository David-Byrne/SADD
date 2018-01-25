import re


def is_tweet_valid(status):
    if status.lang not in ["en", "en-gb"]:
        return False
    if status.user.time_zone not in ["Dublin", None]:
        # if we know they're not in Ireland, should they get a say?
        return False

    try:
        get_tweet_viewpoint(status)
    except ValueError:
        # Tweet must have an illegal number of hashtags
        return False

    return True


def get_tweet_viewpoint(status):
    text = get_tweet_text(status).lower()
    used_hts = re.findall("#\w+", text)
    # This regex is used to match hashtags, it means hash symbol followed by at least
    # one word character

    tracked_hts = {"#repealthe8th", "#savethe8th"}
    if len(tracked_hts.intersection(used_hts)) != 1:
        raise ValueError("Tweet contains wrong number of important hashtags")

    # At this point we know exactly one of the 2 hashtags were used,
    # so we can assume if it's not repeal, then it's save
    return "#repealthe8th" in used_hts


def get_tweet_text(status):
    try:
        tweet_text = _get_status_text(status.retweeted_status)
    except AttributeError:
        tweet_text = _get_status_text(status)

    return tweet_text


def _get_status_text(tweet_status):
    try:
        return tweet_status.extended_tweet["full_text"]
    except AttributeError:
        # if it wasn't a long tweet, just get it the normal way
        return tweet_status.text
