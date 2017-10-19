def is_tweet_valid(status):
    if status.lang not in ["en", "en-gb"]:
        return False
    if status.user.time_zone not in ["Dublin", None]:
        # if we know they're not in Ireland, should they get a say?
        return False
    return True


def get_tweet_text(status):
    try:
        return status.extended_tweet["full_text"]
    except AttributeError:
        # if it wasn't a long tweet, just get it the normal way
        return status.text
