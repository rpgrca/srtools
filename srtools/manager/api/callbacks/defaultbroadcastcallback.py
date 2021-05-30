"""Base callback handler."""
# -*- coding: utf-8 -*-
import json
import codecs
import sys
import time
from datetime import datetime
from srtools.utils.errorprint import print_error

import srtools.manager.api.message

class DefaultBroadcastCallback(object):
    """Base callback handler for the low level conversation with the SHOWROOM server."""
   # Messages
    _MESSAGE_VIEW_COMMENT = 1
    _MESSAGE_THROW_GIFTS = 2
    _MESSAGE_START_VOTE = 3
    _MESSAGE_ENDVOTE = 4
    _MESSAGE_CHANGE_SUPPORT_GAUGE = 5 
    _MESSAGE_SET_TWITTER_ICON = 6
    _MESSAGE_SET_TELOP = 8
    _MESSAGE_HIDE_TELOP = 9
    _MESSAGE_ADD_GIFT_LOG = 11
    _MESSAGE_START_PERFORMANCE_TIME = 12 # No example
    _MESSAGE_START_BRAVO_TIME = 13 # No example
    _MESSAGE_FINISH_BRAVO_TIME = 14 # No example
    _MESSAGE_RESULT_BRAVO_TIME = 15 # No example
    _MESSAGE_SPEAK_BRADARU = 16 # No example
    _MESSAGE_FETCH_AVATAR = 100
    _MESSAGE_END_LIVE = 101
    _UNKNOWNMESSAGE_VOTE_REFRESH = 102
    _MESSAGE_RELOAD_VIDEO = 103
    _MESSAGE_START_LIVE = 104 # No example
    _MESSAGE_VIEW_COMMENT_OLD = 301 # No example
    _MESSAGE_ENTER_OWNER = 302 # No example
    _MESSAGE_LEAVE_OWNER = 303 # No example

    def __init__(self, configuration, room):
        self.configuration = configuration
        self._file = None
        self._alias = "default"
        self._room = room
        self._empty_message_counter = 0
        self._empty_message_limit = 50
        codecs.register_error("customreplace", self._custom_conversion_handler)

    # TODO: Mover esto a showroombroadcast.py, aqui no se usa
    def _custom_conversion_handler(self, ex):
        """
        Handle unicode errors in data.
        :param ex: The string and start/end indexes of the bad portion.
        :type ex: UnicodeDecodeError
        :returns: Tuple of Unicode string and the index to continue conversion.
        """
        # The error handler receives the UnicodeDecodeError, which contains arguments of the
        # string and start/end indexes of the bad portion.
        bstr, start, end = ex.args[1:4]
        # The return value is a tuple of Unicode string and the index to continue conversion.
        # note: iterating byte strings returns int on 3.x but str on 2.x
        return u''.join('\\x{:02x}'.format(c if isinstance(c, int) else ord(c))
                        for c in bstr[start:end]), end

    def _parse_message(self, message):
        """
        Parse message received from SHOWROOM server.
        :param message: Received message.
        :type message: string
        :returns: Array with parsed data.
        :rtype: string[]
        """
        try:
            code = key = data = ""

            count = message.count("\t")
            if count == 2:
                code, key, data = message.split("\t")
            elif count == 1:
                code, data = message.split("\t")
            else:
                code = message.split("\t")

        except Exception as err:
            print_error(err)

        return [code, key, data]

    def _preprocess_message(self, message, code, key, value, respjson):
        """
        Pre-process received message.
        :param message: Original received message.
        :type message: string
        :param code: Message code.
        :type code: int
        :param key: Broadcast key if available.
        :type key: string
        :param value: Unpacked data received.
        :type value: string
        :param respjson: JSON representation of unpacked data.
        :type respjson: string
        :returns: The converted text if possible.
        :rtype: string
        """
        pass

    def _fetch_avatar(self):
        """
        Force fetching all the avatars in the room.
        :returns: True if processing should continue, False if it should stop.
        :rtype: bool
        """
        return True

    def _end_live(self, _anteroomid):
        """
        Terminate current live broadcast.
        :param _anteroomid: Anteroom ID.
        :type _anteroomid: int
        :returns: True if processing should continue, False if it should stop.
        :rtype: bool
        """
        # TODO: Si termina antes de la hora, cargar anteroom y seguir enviando ack
        # hasta que pase una hora
        return False

    def _reload_video(self, _createdat):
        """
        Reload video.
        :param created_at: Time at which it was created (in seconds)
        :type created_at: string
        :returns: True if processing should continue, False if it should stop.
        :rtype: bool
        """
        return True

    def _start_live(self, _value):
        """
        ???
        :param value:
        :returns: True if processing should continue, False if it should stop.
        :rtype: bool
        """
        return True

    def _start_vote(self, _list, _options, _votes):
        """
        {"l":[{"id":10001},{"id":10002},{"id":10003}],"created_at":1499267246,"n":10,"i":3,"t":3}
        Setup a vote.
        :param _list: List of options to display.
                      Each element has: "id": ID of item to display.
        :type _list: dictionary
        :param _options: Amount of options to display.
        :type _options: int
        :param _votes: Amount of votes per option.
        :type _votes: int
        :returns: True if processing should continue, False if it should stop.
        :rtype: bool
        """
        return True


    def _end_vote(self, _results, _imageurl, _version):
        """
        End ballot and show result.
        :param _results: Array of results. Each element has four members:
                         "gr": ?
                         "id": vote number (gift id)
                         "r": Percentage of result
                         "sum": Sum of votes
        :type _results: dictionary
        :param _imageurl: "https://image.showroom-live.com/showroom-prod/assets/img/gift".
        :type _imageurl: string
        :param _version: "v1"?
        :type _version: string
        :returns: True if processing should continue, False if it should stop.
        :rtype: bool
        """
        return True

    def _change_support_gauge(self, _point, _firework):
        """
        Modify the Goal Meter gauge.
        :param _point: Current support point.
        :type _point: int
        :param _firework: 1 if fireworks should be shown, 0 otherwise.
        :type _firework: int
        :returns: True if processing should continue, False if it should stop.
        :rtype: bool
        """
        return True

    def _set_twitter_icon(self, _userid):
        """
        :param _userid: User id.
        :type _userid: int
        :returns: True if processing should continue, False if it should stop.
        :rtype: bool
        """
        return True

    def _add_gift_log(self, _avatarid, _username, _giftid, _quantity):
        """
        Add a new entry at the Special Gift log.
        :param _avatarid: Avatar id.
        :type _avatarid: int
        :param _username: User name.
        :type _username: string
        :param _giftid: Gift id.
        :type _giftid: int
        :param _quantity: Number of thrown items.
        :type _quantity: int
        :returns: True if processing should continue, False if it should stop.
        :rtype: bool
        """
        return True

    def _start_performance_time(self, _pid, _pt, _startedat, _btbpc, _createdat):
        """
        ???
        :param _pid: Time id.
        :type _pid: int
        :param _pt: Performace type.
        :type _pt: ?
        :param _startedat: Start time.
        :type _startedat: string
        :param _btbpc: Background image URL pic.
        :type _btbpc: ?
        :param _createdat: Message time.
        :type _createdat: string
        :returns: True if processing should continue, False if it should stop.
        :rtype: bool
        """
        return True

    def _start_bravo_time(self):
        """
        ???
        :returns: True if processing should continue, False if it should stop.
        :rtype: bool
        """
        return True

    def _finish_bravo_time(self):
        """
        ???
        :returns: True if processing should continue, False if it should stop.
        :rtype: bool
        """
        return True

    def _result_bravo_time(self, _pid, _uu, _tp, _createdat):
        """
        ???
        :param _pid:
        :param _uu:
        :param _tp:
        :param _createdat:
        :returns: True if processing should continue, False if it should stop.
        :rtype: bool
        """
        return True

    def _speak_bradaru(self, _id, _createdat):
        """
        ???
        :param _id:
        :param _created_at:
        :returns: True if processing should continue, False if it should stop.
        :rtype: bool
        """
        return True

    def _view_comment(self, _comment, _username, _userid, _avatarid, _lon, _lat, _rad):
        """
        Comment done by user.
        :param _comment: Posted comment.
        :type _comment: string
        :param _username: User name.
        :type _username: string
        :param _userid: User id.
        :type _userid: int
        :param _avatarid: Avatar id.
        :type _avatarid: int
        :param _lon: None
        :param _lat: None
        :param _rad: None
        :returns: True if processing should continue, False if it should stop.
        :rtype: bool
        """
        return True

    def _throw_gifts(self, _userid, _avatarid, _giftid, _quantity, _username, _showtimeline,
                     _lon, _lat, _rad):
        """
        Throw gift.
        :param _userid: User id.
        :type _userid: int
        :param _avatarid: Avatar id.
        :type _avatarid: int
        :param _giftid: Gift id.
        :type _giftid: int
        :param _quantity: Number of thrown gifts.
        :type _quantity: int
        :param _username: Username.
        :type _username: string
        :param _showtimeline: 1 if it must be shown in the timeline, 0 otherwise.
        :type _showtimeline: int
        :param lon: None
        :param lat: None
        :param rad: None
        :returns: True if processing should continue, False if it should stop.
        :rtype: bool
        """
        return True

    def _set_telop(self, _telop):
        """
        Set new telop.
        :param _telop: Text to show.
        :type _telop: string
        :returns: True if processing should continue, False if it should stop.
        :rtype: bool
        """
        return True

    def _hide_telop(self):
        """
        Hide telop.
        :returns: True if processing should continue, False if it should stop.
        :rtype: bool
        """
        return True

    def _old_view_comment(self, _comment, _username, _userid, _avatarid):
        """
        :param _comment: User comment.
        :type _comment: string
        :param _username: Username.
        :type _username: string
        :param _userid: User id.
        :type _userid: int
        :param _avatarid: Avatar id.
        :type _avatarid: int
        :returns: True if processing should continue, False if it should stop.
        :rtype: bool
        """
        return True

    def _enter_owner(self):
        """
        ???
        :returns: True if processing should continue, False if it should stop.
        :rtype: bool
        """
        return True

    def _leave_owner(self):
        """
        ???
        :returns: True if processing should continue, False if it should stop.
        :rtype: bool
        """
        return True

    def _unknown_vote_refresh(self, _createdat):
        """
        Sent after _start_vote and _end_vote.
        :param _createdat: Message date/time.
        :type _createdat: string
        :returns: True if processing should continue, False if it should stop.
        :rtype: bool
        """
        return True

    def _unknown_message(self, _respjson):
        """
        Unknown message received.
        :param _respjson: JSON of the received message.
        :type _respjson: string
        :returns: True if processing should continue, False if it should stop.
        :rtype: bool
        """
        return True

    def _ack_received(self, _data):
        """
        ACK message received.
        :param _data: The data obtained.
        :type _data: string
        :returns: True if processing should continue, False if it should stop.
        :rtype: bool
        """
        return True

    def _err_received(self):
        """
        ERR message received.
        :returns: True if processing should continue, False if it should stop.
        :rtype: bool
        """
        return True

    def initialize(self):
        """Initialize the object."""
        self._file = None
        if self.configuration.capture.output:
            if self.configuration.capture.output.upper() in ['STDOUT', '-']:
                self._file = sys.stdout
            elif self.configuration.capture.output.upper() == 'STDERR':
                self._file = sys.stderr
            else:
                self._file = open(self.configuration.capture.output, 'a+')

    def terminate(self):
        """Terminate the object."""
        if self.configuration.capture.output is not None:
            self._file.close()

    def alias(self):
        """Return alias of handler."""
        return self._alias

    def new_message(self, message):
        """
        Notification of new message.
        :param message: Received message.
        :type message: string
        """
        self._empty_message_counter = 0
        if self._file:
            self._file.write(str(datetime.now()) + "\t" + message + "\n")

    def empty_message(self):
        """
        Empty message notification.
        :returns: True if communication should still be tried, False otherwise.
        :rtype: bool
        """
        #TODO: Should try to reconnect instead of dropping connection
        cont = True
        self._empty_message_counter += 1
        if self._empty_message_counter > self._empty_message_limit:
            cont = False
            self.new_message("No communication with server, aborting.")
        else:
            time.sleep(1)

        return cont

    def process_message(self, message):
        """
        Process received message.
        :param message: Received message.
        :type message: string
        :returns: True if processing should continue, False if it should stop.
        :rtype: bool
        """
        cont = True
        try:
            #message = message.decode("utf-8", "customreplace")

            code, _key, data = self._parse_message(message)
            if code == srtools.manager.api.message.MESSAGE_HEADER_MSG:
                resp = json.loads(data)
                value = int(resp['t'])

                self._preprocess_message(message, code, _key, value, resp)

                if value == self._MESSAGE_FETCH_AVATAR:
                    cont = self._fetch_avatar()
                elif value == self._MESSAGE_END_LIVE:
                    cont = self._end_live(resp.get('a'))
                elif value == self._MESSAGE_RELOAD_VIDEO:
                    cont = self._reload_video(resp.get('created_at'))
                elif value == self._MESSAGE_START_LIVE:
                    cont = self._start_live("")
                elif value == self._MESSAGE_START_VOTE:
                    cont = self._start_vote(resp.get('l'), resp.get('i'), resp.get('n'))
                elif value == self._MESSAGE_ENDVOTE:
                    cont = self._end_vote(resp.get('l'), resp.get('i'), resp.get('v'))
                elif value == self._MESSAGE_CHANGE_SUPPORT_GAUGE:
                    cont = self._change_support_gauge(resp.get('p'), resp.get('c'))
                elif value == self._MESSAGE_SET_TWITTER_ICON:
                    cont = self._set_twitter_icon(resp.get('u'))
                elif value == self._MESSAGE_ADD_GIFT_LOG:
                    cont = self._add_gift_log(resp.get('av'), resp.get('ac'), resp.get('g'),
                                              resp.get('n'))
                elif value == self._MESSAGE_START_PERFORMANCE_TIME:
                    cont = self._start_performance_time(resp.get('pid'), resp.get('pt'),
                                                        resp.get('sat'), resp.get('btbpc'),
                                                        resp.get('created_at'))
                elif value == self._MESSAGE_START_BRAVO_TIME:
                    cont = self._start_bravo_time()
                elif value == self._MESSAGE_FINISH_BRAVO_TIME:
                    cont = self._finish_bravo_time()
                elif value == self._MESSAGE_RESULT_BRAVO_TIME:
                    cont = self._result_bravo_time(resp.get('pid'), resp.get('uu'), resp.get('tp'),
                                                   resp.get('created_at'))
                elif value == self._MESSAGE_SPEAK_BRADARU:
                    cont = self._speak_bradaru(resp.get('id'), resp.get('created_at'))
                # These are intended for anyone but the current user
                elif value == self._MESSAGE_VIEW_COMMENT:
                    cont = self._view_comment(resp.get('cm'), resp.get('ac'), resp.get('u'),
                                              resp.get('av'), resp.get('lon'), resp.get('lat'),
                                              resp.get('rad'))
                elif value == self._MESSAGE_THROW_GIFTS:
                    cont = self._throw_gifts(resp.get('u'), resp.get('av'), resp.get('g'),
                                             resp.get('n'), resp.get('ac'), resp.get('h'),
                                             resp.get('lon'), resp.get('lat'), resp.get('rad'))
                elif value == self._MESSAGE_SET_TELOP:
                    # "created_at":1499114910
                    # "api":"https://www.showroom-live.com/live/telop?live_id=2035327
                    cont = self._set_telop(resp.get('telop'))
                elif value == self._MESSAGE_HIDE_TELOP:
                    cont = self._hide_telop()
                elif value == self._MESSAGE_VIEW_COMMENT_OLD:
                    cont = self._old_view_comment(resp.get('cm'), resp.get('ac'), resp.get('u'),
                                                  resp.get('av'))
                elif value == self._MESSAGE_ENTER_OWNER:
                    cont = self._enter_owner()
                elif value == self._MESSAGE_LEAVE_OWNER:
                    cont = self._leave_owner()
                elif value == self._UNKNOWNMESSAGE_VOTE_REFRESH:
                    cont = self._unknown_vote_refresh(resp.get('created_at'))
                else:
                    cont = self._unknown_message(resp)
            elif code == srtools.manager.api.message.MESSAGE_HEADER_ACK:
                cont = self._ack_received(data)
            elif code == srtools.manager.api.message.MESSAGE_HEADER_ERR:
                cont = self._err_received()

        except Exception as err:
            print_error(err)

        return cont
