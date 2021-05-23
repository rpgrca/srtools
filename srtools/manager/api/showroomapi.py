"""Connections Manager."""
import re
import uuid
import time
import json
import datetime
#import urllib2
#from lxml import etree
from pytz import timezone
from parse import parse

from srtools.manager.api.showroomwebservice import _ShowroomWebService
from srtools.utils.loggingutils import log_error

class ShowroomAPI(_ShowroomWebService):
    """Showroom API implementation."""
    def query_csrf_token(self):
        """
        :returns: The current valid CSRF token.
        :rtype: string
        """
        return self._query_csrf_token()

    def set_timeout(self, room, timeout):
        """
        Sets timeout.
        :param room: The room to know if it's official or amateur block.
        :type room: Room
        """
        try:
            self.connections_manager.twitter_timeout[room.official] = str(timeout)
        except Exception as err:
            log_error(err)

    def clear_timeout(self, room):
        """
        Clears timeout.
        :param room: The room belonging to the type to clear.
        :type room: Room
        """
        self.connections_manager.twitter_timeout[room.official] = None

    def get_timeout(self, room):
        """
        Returns timeout for given room.
        :param room: Room to check.
        :type room: Room
        :returns: When the bonus ban is lifted, None otherwise.
        :rtype: bool
        """
        return self.connections_manager.twitter_timeout[room.official]

    def do_polling(self, room):
        """
        :param room: The room to query.
        :type room: Room
        :returns: 0 if free items were obtained. 1 if broadcast ended. 2 if nothing, 3 if error.
        :rtype: int
        """
        result = 2
        try:
            respjson = self._query_polling(room).json()
            if respjson.get('live_watch_incentive'):
                if respjson['live_watch_incentive'].get('ok') == 1:
                    self.clear_timeout(room)
                    result = 0
                else:
                    result = 2
            else:
                if respjson.get('invalid') == 1:
                    result = 1
        except ValueError as err:
            result = 3
        except Exception as err:
            result = 3
            log_error(err)

        return result

    def get_current_user(self, room):
        """
        :param room: The room from where to extract the information.
        :type room: Room
        :returns: JSON with the information, None if error or invalid.
        :rtype: string
        """
        respjson = None
        try:
            resp = self._query_current_user(room)
            if resp is not None:
                respjson = resp.json()

                if respjson.get('user_id') == 0 or respjson.get('errors') is not None:
                    respjson = None
        except Exception as err:
            log_error(err)

        return respjson

    def get_onlive_num(self):
        """
        Gets the amount of rooms broadcasting.
        :returns: Amount of live broadcasts, -1 if failed.
        :rtype: int
        """
        result = -1
        try:
            resp = self._query_onlive_num()
            if resp is not None:
                respjson = resp.json()
                result = respjson.get('num')
        except Exception as err:
            log_error(err)

        return result

    def get_onlives(self):
        """
        Gets all the online rooms.
        :returns: JSON with the onlives. None if failed.
        :rtype: string
        """
        respjson = None
        try:
            resp = self._query_onlives()
            if resp is not None:
                respjson = resp.json()
        except Exception as err:
            log_error(err)

        return respjson

    def get_summary_ranking(self, room):
        """
        Gets the historical top 30.
        :param room: The room to query.
        :type room: Room
        :returns: JSON with the ranking, None if not possible.
        :rtype: string
        """
        respjson = None
        try:
            resp = self._query_summary_ranking(room)
            if resp is not None:
                respjson = resp.json()
        except Exception as err:
            log_error(err)

        return respjson

    def get_stage_user_list(self, room):
        """
        Gets the stage user list from a room.
        :param room: The room to query.
        :type room: Room
        :returns: JSON with the people in the room, None if failed.
        :rtype: string
        """
        respjson = None
        try:
            resp = self._query_stage_user_list(room)
            if resp is not None:
                respjson = resp.json()
        except Exception as err:
            log_error(err)

        return respjson

    def get_stage_user_list_anteroom(self, room):
        """
        Gets the anteroom stage user list from a room.
        :param room: The room to query.
        :type room: Room
        :returns: JSON with the people in the room, None if failed.
        :rtype: string
        """
        respjson = None
        try:
            resp = self._query_stage_user_list_anteroom(room)
            if resp is not None:
                respjson = resp.json()
        except Exception as err:
            log_error(err)

        return respjson

    def get_stage_gift_list(self, room):
        """
        Gets the stage gift list from a room (towers and above).
        :param room: The room to query.
        :type room: Room
        :returns: JSON with the gifts in the room, None if failed.
        :rtype: string
        """
        respjson = None
        try:
            resp = self._query_stage_gift_list(room)
            if resp is not None:
                respjson = resp.json()
        except Exception as err:
            log_error(err)

        return respjson

    def get_gift_list(self, room):
        """
        Gets the gift list of the given room.
        :param room: The room to query.
        :type room: Room
        :returns: JSON with the gift list, none if failed.
        :rtype: string
        """
        respjson = None
        try:
            resp = self._query_gift_list(room)
            if resp is not None:
                respjson = resp.json()
        except Exception as err:
            log_error(err)

        return respjson

    def get_setings(self, room):
        """
        Gets settings for the room.
        :param room: The room to query.
        :type room: Room
        :returns: JSON with available performance types, None if failed.
        :rtype: string
        """
        respjson = None
        try:
            resp = self._query_settings(room)
            if resp is not None:
                respjson = resp.json()
        except Exception as err:
            log_error(err)

        return respjson

    def get_telop(self, room):
        """
        Gets the telop for the requested room.
        :param room: The room to query.
        :type room: Room
        :returns: The telop text if found, empty if not.
        :rtype: string
        """
        result = ''
        try:
            resp = self._query_telop(room)
            if resp is not None:
                respjson = resp.json()
                result = respjson.get('telop')
        except Exception as err:
            log_error(err)

        return result

    def get_event_and_support(self, room):
        """
        Gets the event information of the room.
        :param room: The room to query.
        :type room: Room
        :returns: JSON, or None if failed.
        :rtype: string
        """
        respjson = None
        try:
            resp = self._query_event_and_support(room)
            if resp is not None:
                respjson = resp.json()
        except Exception as err:
            log_error(err)

        return respjson

    def get_gift_log(self, room):
        """
        Gets the gift log from the room.
        :param room: The room to query.
        :type room: Room
        :returns: JSON, or None if failed.
        :rtype: string
        """
        respjson = None
        try:
            resp = self._query_gift_log(room)
            if resp is not None:
                respjson = resp.json()
        except Exception as err:
            log_error(err)

        return respjson

    def get_questionnaire_result(self, room):
        """
        Gets the result of a questionnaire.
        :param room: The room to query.
        :type room: Room
        :returns: JSON, or None if failed.
        :rtype: string
        """
        respjson = None
        try:
            resp = self._query_questionnaire_result(room)
            if resp is not None:
                respjson = resp.json()
        except Exception as err:
            log_error(err)

        return respjson

    def get_user_profile(self, room, user):
        """
        Gets user profile from given room.
        :param room: Room to query.
        :type room: Room
        :param user: User to query.
        :type user: User
        :returns: HTML with popup
        :rtype: string
        """
        try:
            result = self._query_user_profile(room, user)
        except Exception as err:
            log_error(err)
            result = None

        return result

    def get_comment_log(self, room):
        """
        Gets the room's comment log.
        :param room: Room to query.
        :type room: Room
        :returns: JSON, or None if failed.
        :rtype: string
        """
        respjson = None
        try:
            resp = self._query_comment_log(room)
            if resp is not None:
                respjson = resp.json()
        except Exception as err:
            log_error(err)
            respjson = None

        return respjson

    def get_banners(self, room):
        """
        Gets the banners of the room.
        :param room: Room to query.
        :type room: Room
        :returns: JSON, or None if failed.
        :rtype: string
        """
        try:
            result = self._query_banners(room)
        except Exception as err:
            log_error(err)
            result = None

        return result

    def refresh_token(self):
        """
        Updates the csrf token if necessary.
        :returns: Whether a new token was obtained or not.
        :rtype: bool
        """
        result = False
        try:
            resp = self.connections_manager.get("https://www.showroom-live.com")
            token = re.search('name="csrf_token" value="([^"]*)"', resp.content).groups()[0]

            if self.query_csrf_token() != token:
                print(f"Refreshing csrf_token from {self.query_csrf_token()} to {token}.")
                self.current_csrf_token = token
            else:
                print(f"Current csrf_token {self.query_csrf_token()} still valid.")

            result = True

        except Exception as _err:
            print(f"Could not refresh csrf_token, using default {self.query_csrf_token()}.")

        return result

    def can_get_bonus(self, room):
        """
        Check whether bonus can be obtained.
        :param room: The room from where to check.
        :type room: Room
        :returns: True if it can be obtained, False otherwise.
        :rtype: bool
        """
        if not self.connections_manager.forbidden:
            result = True

            if self.connections_manager.twitter_timeout[room.official] is not None:
                japan_time = datetime.datetime.now(tz=timezone('Asia/Tokyo')).time()

                result = (self.connections_manager.twitter_timeout[room.official] < japan_time)
                if result:
                    self.connections_manager.twitter_timeout[room.official] = None
        else:
            result = False

        return result

    def is_online(self, room_id):
        """
        Checks if the given room is online.
        :param room_id: The room id to query.
        :type room_id: int
        :returns: True if it's online, False otherwise.
        :rtype: bool
        """
        result = False
        try:
            resp = self._query_is_online(room_id)
            if resp is not None:
                respjson = resp.json()
                result = (respjson.get('ok') == 1)
                #result = (respjson.get('live_status') == 2)
        except Exception as err:
            log_error(err)

        return result

    def login(self, username, password):
        """Login."""
        result = False

        try:
            if self.refresh_token():

                resp = self._query_login(username, password)
                if resp is not None:
                    respjson = resp.json()
                    if respjson.get("ok") == 1:
                        result = True
                    elif respjson.get("error") == 'Already logged in.':
                        result = True

        except Exception as err:
            log_error(err)

        return result

    def get_live(self, room, lives_manager):
        """
        Returns broadcast id from given room.
        :param room: The room to query.
        :type room: Room
        :param lives_manager: Current lives manager.
        :type lives_manager: LivesManager
        :returns: Live object.
        :rtype: Live
        """
        result = None
        try:
            if self.is_online(room.room_id):
                data = self._query_live_data(room).json()
                live_id = int(data['live_id'])
                result = lives_manager.find(live_id)

                if result is None:
                    result = lives_manager.create(live_id)

            room.live = result
        except Exception as err:
            log_error(err)

        return result

    def get_live_data(self, room, lives_manager):
        """
        Returns broadcast information from given room.
        :param room: The room to query.
        :type room: Room
        :param lives_manager: Current lives manager.
        :type lives_manager: LivesManager
        :returns: Live object.
        :rtype: Live
        """
        result = None
        try:
            respjson = None

            if self.is_online(room.room_id):
                resp = self._query_live_data(room)
                if resp is not None:
                    respjson = resp.json()
                    live_id = int(respjson['live_id'])
                    result = lives_manager.find(live_id)

                    if result is None:
                        result = lives_manager.create(live_id)

                    lives_manager.refresh(result, respjson)
        except Exception as err:
            log_error(err)

        return result

    def send_comment(self, live, comment, max_tries=5, delay=1):
        """
        Sends the given comment to the given broadcast.
        :param live: Live object where to send the comment.
        :type live: Live
        :param comment: Comment to send.
        :type comment: string
        :param max_tries: Maximum amount of tries to send the comment.
        :type max_tries: int
        :returns: True if it could be sent, False otherwise.
        :rtype: bool
        """
        result = False
        if max_tries < 1:
            max_tries = 1

        while not result and max_tries > 0:
            max_tries -= 1

            try:
                resp = self._query_comment(live, comment)
                respjson = resp.json()
                result = (respjson.get('ok') == 1)
                if not result:
                    print(respjson)
                    if respjson.get('errors'):
                        if (respjson['errors'][0].get('error_user_msg') == \
                            'This show has already ended.') or \
                           (respjson['errors'][0].get('error_user_msg') == \
                            'Commenting is not available') :
                            break
                        elif respjson['errors'][0].get('error_user_msg') == 'Please try again.':
                            time.sleep(delay)
            except Exception as err:
                log_error(err)

        return result

    def parse_timeout_error(self, room, error_message):
        """
        Parse error message and set timeout.
        :param room: Room from where to check.
        :type room: Room
        :param error_message: Error message to parse.
        :type error_message: string
        """
        try:
            waiting = parse("You can get free gifts until {}.", error_message)
            if waiting:
                self.set_timeout(room, datetime.datetime.strptime(waiting[0], "%H:%M").time())
        except Exception as err:
            log_error(err)

    def send_tweet(self, room, comment=None):
        """
        Send tweet from the current room.
        :param room: The room from where to tweet.
        :type room: Room
        :param comment: The comment to send.
        :type comment: string
        :returns: True if bonus was gotten, False otherwise.
        :rtype: bool
        """
        result = False

        if comment is None:
            uuid_value = str(uuid.uuid4())
            tweet_default = room.live.tweet_default if room.live and room.live.tweet_default \
                                                    else room.name + " Broadcasting!\n"
            comment = tweet_default + uuid_value if len(tweet_default) + len(uuid_value) < 140 \
                                                 else tweet_default[:-36] + uuid_value

        resp = self._query_tweet(room, comment)
        try:
            respjson = resp.json()
            if respjson.get('ok') == 1:
                room.badge = True

                # {u'add': 1, u'ok': 1}
                # {u'add': 0, u'ok': 1}
                result = (respjson.get('add') == 1)
                if result:
                    self.clear_timeout(room)
            else:
                # {u'api_error': 1, u'error': u'You can get free g...il 02:54.'}
                if respjson.get('api_error') == 1:
                    if (respjson['error'] != u'\u6295\u7a3f\u306b\u5931\u6557\u3057\u307e\u3057\u305f\u3002') and (respjson['error'] != "posting failed"):
                        self.parse_timeout_error(room, respjson['error'])
        except Exception as err:
            log_error(err)

        return result

    def update_profile(self, profile_configuration):
        """
        :param profile_configuration: Configuration to use.
        :type profile_configuration: ProfileConfiguration
        :returns: True if the profile could be updated, False otherwise.
        :rtype: bool
        """
        try:
            result = False
            if profile_configuration.avatar_id != None and profile_configuration.name != None:
                resp = self._query_profile(profile_configuration)
                result = (resp.url == u'https://www.showroom-live.com/user/my_profile_edit_done')
        except Exception as err:
            log_error(err)

        return result

    def get_next_live(self, room_id):
        """
        :param room_id: Room to check.
        :type room_id: int
        :returns: The scheduled date for next broadcast, None if not available.
        :rtype: datetime.datetime
        """
        result = None
        try:
            resp = self._query_next_live(room_id)
            if resp is not None:
                result = resp.json().get('epoch')

                if result is not None:
                    result = datetime.datetime.fromtimestamp(result)
        except Exception as err:
            log_error(err)

        return result

    def throw_free_gift(self, live, gift_id, num):
        """
        Throw free gift to given live.
        :param live: Live where to throw the gift.
        :type live: Live
        :param gift_id: Gift id to throw.
        :type gift_id: int
        :param num: Amount of items to throw.
        :type num: int
        """
        result = None
        try:
            resp = self._query_gifting_free(live, gift_id, num)
            if resp is not None:
                respjson = resp.json()
                if respjson.get('ok'):
                    text = {
                        'ok': respjson['ok'],
                        'level': respjson['fan_level']['fan_level'],
                        'point': respjson['fan_level']['contribution_point'],
                        'levelup': respjson['notify_level_up'],
                        'gift_id': respjson['gift_id'],
                        'remaining': respjson['remaining_num']
                    }

                    result = json.loads(json.dumps(text))
                elif respjson.get('errors'):
                    result = respjson
                    log_error('Errors (%s)' % respjson.get('errors'))
                elif respjson.get('error'):
                    result = respjson
                    log_error('Error (%s)' % respjson.get('error'))

        except Exception as err:
            log_error(err)

        return result

    def throw_paid_gift(self, live, gift_id, num):
        """
        Throw paid gift to given live.
        :param live: Live where to throw the gift.
        :type live: Live
        :param gift_id: Gift id to throw.
        :type gift_id: int
        :param num: Amount of items to throw.
        :type num: int
        """
        result = None
        try:
            resp = self._query_gifting_point_use(live, gift_id, num)
            if resp is not None:
                result = resp.json()
        except Exception as err:
            log_error(err)

        return result

    def execute_lottery(self, lottery):
        """
        Execute requested lottery.
        :param lottery: The lottery to play.
        :type lottery: string
        :returns: The JSON with the reply.
        :rtype: string
        """
        result = None
        try:
            resp = self._query_lottery(lottery)
            if resp is not None:
                result = resp.json()
                if result.get('error') == 1:
                    result = None
        except Exception as err:
            log_error(err)

        return result

    def update_user_avatar(self, avatar_id):
        """
        Updates the user avatar.
        :param avatar_id: The id of the avatar to use.
        :type avatar_id: string
        :returns: The JSON with the reply.
        :rtype: string
        """
        result = None
        try:
            resp = self._query_update_user_avatar(avatar_id)
            if resp is not None:
                result = resp.json()
                if result.get('error') == 1:
                    result = None
        except Exception as err:
            log_error(err)

        return result
