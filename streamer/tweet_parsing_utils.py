def is_tweet_valid(status):
    if status.lang not in ["en", "en-gb"]:
        return False
    if status.user.time_zone not in ["Dublin", None]:
        # if we know they're not in Ireland, should they get a say?
        return False

    tracked_hts = {"repealthe8th", "savethe8th"}
    used_hts = [ht["text"].lower() for ht in status.entities["hashtags"]]
    if len(tracked_hts.intersection(used_hts)) != 1:
        # either they didn't contain any of the hashtags we're searching for or
        # they contain more than one hashtag we're looking for which would be noise
        return False

    return True


def get_tweet_text(status):
    try:
        return status.extended_tweet["full_text"]
    except AttributeError:
        # if it wasn't a long tweet, just get it the normal way
        return status.text
