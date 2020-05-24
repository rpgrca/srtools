"""Colored output."""
# -*- coding: utf-8 -*-
from datetime import datetime
from colorama import Fore, Back
from srtools.manager.api.callbacks.defaultbroadcastcallback import DefaultBroadcastCallback
from srtools.utils.jsonutils import load_json
from srtools.utils.errorprint import print_error

class WatchBroadcastCallback(DefaultBroadcastCallback):
    """ANSI colored output."""
    def __init__(self, configuration, room):
        super(WatchBroadcastCallback, self).__init__(configuration, room)

        self._alias = "watch"
        self._official_users = self._load_users("srtools/resources/fav_official_users.json")
        self._myself = self._load_users("srtools/resources/myself.json")

    def _load_users(self, filename):
        respjson = load_json(filename)
        if respjson is None:
            print_error("No %s loaded!", filename)
            respjson = {}

        return respjson

    def _check_if_official(self, user):
        """
        Check if given user is 48G-related.
        :param user: user id.
        :type user: int
        :returns: True if the user is 48G official, False otherwise.
        :rtype: bool
        """
        return str(user) in self._official_users
        #09:57:11.5008799NANIHIKO (777545) wrote in room 48_ISOGAI_KANON: 
        # no es official user pero se mostro, por que?

    def _check_if_myself(self, user):
        """
        Check if given user is onself.
        :param user: user id.
        :type user: int
        :returns: True if the user is 48G official, False otherwise.
        :rtype: bool
        """
        return str(user) in self._myself

    def _preprocess_message(self, message, code, key, value, respjson):
        user = respjson.get("u")

        if self._check_if_official(user):
            result = str(datetime.now().time()) + "\t" + message
            print_error(Fore.LIGHTWHITE_EX + Back.RED + result + Fore.RESET + Back.RESET)
        elif self._check_if_myself(user):
            result = str(datetime.now().time()) + "\t" + message
            print_error(Fore.LIGHTWHITE_EX + Back.GREEN + result + Fore.RESET + Back.RESET)
        else:
            result = ""

        return result
