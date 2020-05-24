"""Colored output."""
#!/usr/bin/env python
# vim:set fileencoding=UTF-8
from datetime import datetime
from colorama import Fore, Back
from srtools.manager.api.callbacks.trackbroadcastcallback import TrackBroadcastCallback
from srtools.utils.throwableitems import throwable_item_name
from srtools.utils.errorprint import print_error

class ReadableBroadcastCallback(TrackBroadcastCallback):
    """Human readable output."""
    def __init__(self, configuration, room):
        super(ReadableBroadcastCallback, self).__init__(configuration, room)
        self._alias = "readable"

    def _preprocess_message(self, message, code, key, value, respjson):
        user = respjson.get("u")
        text = respjson.get("cm")

        start_color = end_color = None

        if self._check_if_official(user):
            start_color = Fore.LIGHTWHITE_EX + Back.RED
            end_color = Fore.RESET + Back.RESET
        elif self._check_if_myself(user):
            start_color = Fore.LIGHTWHITE_EX + Back.GREEN
            end_color = Fore.RESET + Back.RESET

        if start_color and end_color:
            value = int(value)
            if value == self._MESSAGE_VIEW_COMMENT:
                text = "%s (%s) wrote in room %s: %s" % (respjson.get("ac"), respjson.get("u"), \
                                                        self._room.room_url_key, respjson.get("cm"))
            elif value == self._MESSAGE_THROW_GIFTS:
                text = "%s (%s) threw in room %s %s item %s." % \
                    (respjson.get("ac"), respjson.get("u"), self._room.room_url_key, \
                    respjson.get("n"), throwable_item_name(respjson.get("g")))
            else:
                text = message

            result = str(datetime.now().time()) + "\t" + text
            print_error(start_color + result + end_color)
