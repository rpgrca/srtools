"""Colored output."""
from datetime import datetime
from colorama import Fore, Back
from srtools.utils.errorprint import print_error
from srtools.manager.api.callbacks.watchbroadcastcallback import WatchBroadcastCallback
from srtools.configuration.configuration import FreeGifts, BallotGifts

class ColoredBroadcastCallback(WatchBroadcastCallback):
    """ANSI colored output."""
    def __init__(self, configuration, room):
        super(ColoredBroadcastCallback, self).__init__(configuration, room)
        self._free_items = [e.value for e in FreeGifts] + [e.value for e in BallotGifts]
        self._alias = "colored"

    def _preprocess_message(self, message, code, key, value, respjson):
        date = str(datetime.now().time())
        color_begin = ""
        color_end = ""
        official_user_detected = False
        user = respjson.get("u")

        if self._check_if_official(user):
            color_begin = Fore.LIGHTWHITE_EX + Back.RED
            color_end = Fore.RESET + Back.RESET
            official_user_detected = True
        elif self._check_if_myself(user):
            color_begin = Fore.LIGHTWHITE_EX + Back.GREEN
            color_end = Fore.RESET + Back.RESET
        else:
            if value == self._MESSAGE_THROW_GIFTS:
                if respjson.get("g") in self._free_items:
                    color_begin = Fore.GREEN
                    color_end = Fore.RESET
                else:
                    color_begin = Fore.LIGHTGREEN_EX
                    color_end = Fore.RESET

            elif value == self._MESSAGE_VIEW_COMMENT:
                color_begin = Fore.YELLOW
                color_end = Fore.RESET
            elif value == self._MESSAGE_SET_TWITTER_ICON:
                color_begin = Fore.LIGHTCYAN_EX
                color_end = Fore.RESET
            else:
                color_begin = ""
                color_end = ""

        value = color_begin + date + "\t" + message + color_end
        if official_user_detected:
            print_error(value)
        else:
            print value
