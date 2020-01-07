
ok_status = [200, 302, 301]
timeout_status = [210, ]
blacklist_words = [
    "was deleted",
    # "removed",
    # "invalid",
    "invalid file",
    # "failed",
    "has not been found",
    "has been blocked",
    "try again later",
    "no source available",
    "dmca takedown",
    "copyright violation",
    "video not found or removed",  # ok.ru
    "does not exist",  # gcloud
    "we are sorry",  # mixdrop
    "we're sorry",#vidcloud.co
    "video has not been found",
    "404 Page not found", #uptostream,
    "File not found", #vidcloud
    "Oops! Sorry",
    "File you are looking for is not found", #onlystream
    "not found", #vidsrc
    "This video has been deleted", #vev.red
    "File is no longer available as it expired or has been deleted.", # newsexit
    "Looks like we lost one.",
    "missing video id", #gcloud.live
    "404. PAGE NOT FOUND",
    "File code was changed, please check your account and Update embed code on your site.",# prostream.to
    "We can't find the video you are looking for.",#mixdrop.co
    "We cant give you what you looking for.",#oyohd
    "ERROR 2",#player.clipot.tv
    "File is no longer available as it expired or has been deleted.", #newsexit
]


def check_host(response):

    data = {**response.meta}
    broken = {
        **data, "broken": True,
        "perform_operation": True,
        "operation": "update",
        "new_source": {"report_verified": True}
    }
    not_broken = {**data, "broken": False, "perform_operation": False}

    if response.status in timeout_status:
        if data["retry_count"] > 2:
            return broken
        return {**not_broken, "retry": True,
                "retry_count": broken["retry_count"] + 1 if broken["retry_count"] else 1}

    if response.status not in ok_status:
        return broken

    content = response.text.lower()

    is_broken = False
    for black_word in blacklist_words:
        if black_word.lower() in content:

            is_broken = True
            print(is_broken, black_word)
    if is_broken:
        return broken
    return not_broken
