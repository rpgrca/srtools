"""Base Manager"""
class BaseManager(object):
    """Base Manager."""
    def __init__(self, configuration, showroom_api):
        """
        Initialization
        :param configuration: Configuration to use.
        :type configuration: Configuration
        :param showroom_api: Showroom API to use.
        :type showroom_api: ShowroomAPI
        """
        self.configuration = configuration
        self.showroom_api = showroom_api
