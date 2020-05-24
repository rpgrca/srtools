"""Colored output."""
#!/usr/bin/env python
# vim:set fileencoding=UTF-8
from datetime import datetime
from colorama import Fore, Back
from srtools.manager.api.callbacks.watchbroadcastcallback import WatchBroadcastCallback
from srtools.utils.errorprint import print_error

class TrackBroadcastCallback(WatchBroadcastCallback):
    """ANSI colored output."""
    # define colors as unicode here, for example
    MORI = u'\u304b'

    def __init__(self, configuration, room):
        super(TrackBroadcastCallback, self).__init__(configuration, room)
        self._alias = "track"

    def _preprocess_message(self, message, code, key, value, respjson):
        super(TrackBroadcastCallback, self)._preprocess_message(message, code, key, value, respjson)

        text = respjson.get("cm")
        if text is not None:
            if text.find(self.MORI) > -1:
                result = str(datetime.now().time()) + "\t" + message
                print_error(Fore.LIGHTWHITE_EX + Back.YELLOW + result + Fore.RESET + Back.RESET)
