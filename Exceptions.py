class PersonNotFound(Exception):
    """Entered username was not found on Anilist"""
    pass


class ImagesDownloadFailed(Exception):
    """Error happened while downloading images"""
    pass
