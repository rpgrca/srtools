"""Connections Manager."""
import time
from collections import OrderedDict
import requests
from requests.exceptions import ConnectionError
import browsercookie

from srtools.utils.loggingutils import log_error

# Hack to be able to use request against showroom-live.com
# code taken from https://stackoverflow.com/questions/38015537/python-requests-exceptions-sslerror-dh-key-too-small
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass

class _ShowroomWebService(object):
    """Interface to interact with Showroom API."""
    _CSRF_TOKEN = '' # add csrf token of used browser

    # Web pages
    WEB_USER_PROFILE = "https://www.showroom-live.com/room/user_profile"
    # API
    API_ROOM_PROFILE = "https://www.showroom-live.com/api/room/profile" # https://www.showroom-live.com/api/room/profile?room_id=24798&_=1554695144606
    API_ANTEROOM_COMMENTS = "https://www.showroom-live.com/api/anteroom/comments"
    API_ANTEROOM_POST_COMMENT = "https://www.showroom-live.com/api/anteroom/comments"
    API_ANTEROOM_STAGE_USER_LIST = "https://www.showroom-live.com/api/anteroom/stage_user_list"
    API_ANTEROOM_POLLING = "https://www.showroom-live.com/anteroom/polling"
    API_TIME_TABLE = "https://www.showroom-live.com/api/time_table/time_tables"
    # ?order=asc&ended_at=1496285999&_=1494730171439
    API_BANNERS = "https://www.showroom-live.com/api/room/banners"
    API_COMMENT_LOG = "https://www.showroom-live.com/api/live/comment_log"
    API_CURRENT_USER = "https://www.showroom-live.com/api/live/current_user"
    API_ENQUETE_RESULT = "https://www.showroom-live.com/api/live/enquete_result"
    API_EVENT_AND_SUPPORT = "https://www.showroom-live.com/api/room/event_and_support"
    API_GET_LIVE_DATA = "https://www.showroom-live.com/api/room/get_live_data" # ouch, deleted
    API_LIVE_INFO = "https://www.showroom-live.com/api/live/live_info"
    API_STATUS = "https://www.showroom-live.com/api/room/status"
    API_GIFTING_FREE = "https://www.showroom-live.com/api/live/gifting_free"
    API_GIFTING_POINT_USE = "https://www.showroom-live.com/api/live/gifting_point_use"
    API_GIFT_LIST = "https://www.showroom-live.com/api/live/gift_list"
    API_GIFT_LOG = "https://www.showroom-live.com/api/live/gift_log"
    API_IS_LIVE = "https://www.showroom-live.com/room/is_live"
    API_LOGIN = "https://www.showroom-live.com/user/login"
    API_LOGOUT = "https://www.showroom-live.com/user/logout_api"
    API_TRACKER_LOG = "https://www.showroom-live.com/tracker/log"
    API_LOGOUT = "https://www.showroom-live.com/user/logout_api"
    API_NEXT_LIVE = "https://www.showroom-live.com/api/room/next_live"
    API_ONLIVE_NUM = "https://www.showroom-live.com/api/live/onlive_num"
    API_ONLIVES = "https://www.showroom-live.com/api/live/onlives"
    API_POLLING = "https://www.showroom-live.com/api/live/polling"
    API_POST_LIVE_COMMENT = "https://www.showroom-live.com/api/live/post_live_comment"
    API_POST_TWEET = "https://www.showroom-live.com/social/twitter/post_tweet"
    API_PROFILE_EDIT = "https://www.showroom-live.com/user/my_profile_edit"
    API_SETTINGS = "https://www.showroom-live.com/api/room/settings"
    API_STAGE_GIFT_LIST = "https://www.showroom-live.com/api/live/stage_gift_list"
    API_STAGE_USER_LIST = "https://www.showroom-live.com/api/live/stage_user_list"
    API_SUMMARY_RANKING = "https://www.showroom-live.com/api/live/summary_ranking"
    API_TELOP = "https://www.showroom-live.com/api/live/telop"
    API_TWITTER_IS_FOLLOWING = "https://www.showroom-live.com/social/twitter/is_following"
    API_LOTTERY = "https://www.showroom-live.com/lottery/exec"
    API_FOLLOW_ROOM = "https://www.showroom-live.com/api/room/follow"
    API_IMAGE_AND_VOICE = "https://www.showroom-live.com/api/room/image_and_voice"
    API_RECOMMEND_COMMENTS = "https://www.showroom-live.com/api/room/recommend_comments"
    API_UPDATE_USER_AVATAR = "https://www.showroom-live.com/api/user/update_user_avatar"
    API_EVENT_ROOM_LIST = "https://www.showroom-live.com/event/room_list"
#POST /api/user/update_user_avatar HTTP/1.1
#POST /lottery/exec k=2017_spring&csrf_token=vCqkmjQEpyg13ez0YlzBxFB1bOsaFxMwImJAl0eE

    current_csrf_token = None

    class ConnectionsManager(object):
        """Connections Manager."""
        def __init__(self, configuration, session=None):
            # 0: Amateur, 1: Official
            self.twitter_timeout = [None, None]
            self.forbidden = False
            self.configuration = configuration

            if session is None:
                self.session = requests.Session()
                if self.configuration.connection.cookies == "firefox":
                    self.session.cookies = browsercookie.firefox()
                elif self.configuration.connection.cookies == "chrome":
                    self.session.cookies = browsercookie.chrome()

                #self.session.cookies = browsercookie.chrome()
            else:
                self.session = session

        def _get_proxies(self):
            proxies = {
                #'http': "socks5://127.0.0.1:9050",
                #'https': "socks5://127.0.0.1:9050"
            }

            return proxies

        def _get_http_headers(self):
            """Returns modified headers for HTTP connection."""
            headers = requests.utils.default_headers()
            headers.update({
                'User-Agent': self.configuration.connection.user_agent,
                'Origin': "https://www.showroom-live.com",
                'Host': "www.showroom-live.com",
                'DNT': '1',
                'X-Requested-With' : 'XMLHttpRequest',
                'Referer': "https://www.showroom-live.com/onlive",
            })
            return headers

        def get(self, url, **kwargs):
            """Executes a GET query."""
            result = None
            if not self.forbidden:
                count = 0
                while count < self.configuration.connection.retries:
                    count += 1

                    try:
                        #log_trace("HTTP GET", extra='{url: %s, params=%s}' % (url, str(kwargs)))
                        result = self.session.get(url,
                                                  timeout=self.configuration.connection.timeout,
                                                  headers=self._get_http_headers(),
                                                  proxies=self._get_proxies(), **kwargs)
                        if result.status_code == 200:
                            pass
                        if result.status_code == 403:
                            self.forbidden = True
                        if result.status_code == 404:
                            pass
                        break
                    except ConnectionError as err:
                        log_error(err)
            return result

        def post(self, url, **kwargs):
            """Executes a POST query."""
            result = None
            if not self.forbidden:
                count = 0
                while count < self.configuration.connection.retries:
                    count += 1

                    try:
                        result = self.session.post(url,
                                                   timeout=self.configuration.connection.timeout,
                                                   headers=self._get_http_headers(),
                                                   proxies=self._get_proxies(), **kwargs)
                        if result.status_code == 200:
                            pass
                            #result_json = result.json()
                        if result.status_code == 403:
                            result = None
                            self.forbidden = True
                        break
                    except ConnectionError as err:
                        log_error(err)
                        break

            return result

    def __init__(self, configuration, session=None):
        self.connections_manager = self.ConnectionsManager(configuration, session)
        self.current_csrf_token = self._CSRF_TOKEN

    def _query_csrf_token(self):
        """
        Return current CSRF token.
        :returns: The current token.
        :rtype: string
        """
        return self.current_csrf_token

    def _query_lottery(self, lottery):
        """Queries lottery."""
        data = {
            'k': lottery,
            'csrf_token' : self._query_csrf_token()
        }
        return self.connections_manager.post(self.API_LOTTERY, data=data)

    def _query_onlives(self):
        """Queries onlives."""
        params = {
            'skip_serial_code_live': 1,
            '_': int(time.time())
        }
        #params = {
        #    '_': int(time.time())
        #}
        return self.connections_manager.get(self.API_ONLIVES, params=params)

    def _query_anteroom_comments(self, room, anteroom):
        """Get anteroom comments."""
        params = {
            'room_id': room.room_id,
            'anteroom_id': anteroom.room_id,
            '_': int(time.time())
        }
        return self.connections_manager.get(self.API_ANTEROOM_COMMENTS, params=params)

    def _query_anteroom_post_comments(self, room, anteroom, comment):
        """Sends a comment to the given anteroom."""
        data = {
            'room_id': room.room_id,
            'anteroom_id': anteroom.room_id,
            'comment': comment,
            'csrf_token': self._query_csrf_token()
        }
        return self.connections_manager.post(self.API_ANTEROOM_POST_COMMENT, data=data)

    def _query_anteroom_polling(self, room, anteroom, _comment):
        """Polls the given anteroom."""
        data = {
            'room_id': room.room_id,
            'anteroom_id': anteroom.room_id,
            'heartbeat': int(time.time()),
            'csrf_token': self._query_csrf_token()
        }
        return self.connections_manager.post(self.API_ANTEROOM_POLLING, data=data)

    def _query_timetable(self):
        """Queries timetable."""
        params = {
            'order': 'asc',
            'ended_at': int(time.time()),
            '_': int(time.time())
        }
        return self.connections_manager.get(self.API_TIME_TABLE, params=params)
       # ?order=asc&ended_at=1496285999&_=1494730171439

    def _query_onlive_num(self):
        """Queries onlive num."""
        return self.connections_manager.get(self.API_ONLIVE_NUM, params={'_':int(time.time())})
        # {u'num': 165}

    def _query_banners(self, room):
        """Queries the banners of the room."""
        return self.connections_manager.get(self.API_BANNERS, params={'room_id': room.room_id})

    def _query_current_user(self, room):
        """Queries current_user."""
        params = {
            'room_id': room.room_id,
            '_': int(time.time())
        }
        return self.connections_manager.get(self.API_CURRENT_USER, params=params)

    def _query_polling(self, room):
        """Polls current room."""
        params = {
            'room_id': room.room_id,
            '_': int(time.time())
        }
        return self.connections_manager.get(self.API_POLLING, params=params)

    def _query_event_room_list(self, event_id, page):
        """Gets a list of rooms in an event."""
        params = {
            'event_id': event_id,
            'p': page
        }
        return self.connections_manager.get(self.API_EVENT_ROOM_LIST, params=params)

    def _query_twitter_is_following(self, user):
        """Returns if following twitter."""
        data = {
            'user_id': user.user_id,
            'csrf_token': self._query_csrf_token()
        }
        return self.connections_manager.post(self.API_TWITTER_IS_FOLLOWING, data=data)

    def _query_follow_room(self, room, flag):
        """Follows the given room."""
        data = {
            'room_id': room.room_id,
            'flag': flag,
            'csrf_token': self._query_csrf_token()
        }
        return self.connections_manager.post(self.API_FOLLOW_ROOM, data=data)

    def _query_image_and_voice(self, room):
        """Gets images and voices from fan room."""
        params = {
            'room_id': room.room_id
        }
        return self.connections_manager.get(self.API_IMAGE_AND_VOICE, params=params)

    def _query_user_profile(self, room, user):
        """Gets user profile popup for the given user in the given room."""
        params = {
            'room_id': room.room_id,
            'user_id': user.user_id,
            '_': int(time.time())
        }
        return self.connections_manager.get(self.WEB_USER_PROFILE, params=params)

    def _query_recommend_comments(self, room, page, next):
        """Gets recommendations for given room."""
        params = {
            'room_id': room.room_id,
            'page': page,
            'next': next
        }
        return self.connections_manager.get(self.API_RECOMMEND_COMMENTS, params=params)

    def _query_event_and_support(self, room):
        """Gets event and support from room."""
        params = {
            'room_id': room.room_id,
            '_': int(time.time())
        }
        return self.connections_manager.get(self.API_EVENT_AND_SUPPORT, params=params)

    def _query_is_online(self, room_id):
        """Pools whether the room is online or not."""
        return self.connections_manager.get(self.API_IS_LIVE, params={"room_id": room_id})
        #params = {"room_id": room_id}
        #return self.connections_manager.get(self.API_LIVE_INFO, params=params)

    def _query_live_data(self, room):
        """Queries information for the current room."""
        #params = {"room_id": room.room_id}
        #return self.connections_manager.get(self.API_GET_LIVE_DATA, params=params)
        return self._query_live_info(room)

    def _query_live_info(self, room):
        """Queries information for the current room."""
        params = {"room_id": room.room_id}
        return self.connections_manager.get(self.API_LIVE_INFO, params=params)

    def _query_status(self, room):
        """Queries information for the current room."""
        params = {"room_url_key": room.room_url_key}
        return self.connections_manager.get(self.API_STATUS, params=params)

    def _query_comment(self, live, comment):
        """Sends a comment to the given broadcast."""
        data = {
            'live_id' : str(live.live_id),
            'comment' : comment,
            'csrf_token' : self._query_csrf_token()
        }

        return self.connections_manager.post(self.API_POST_LIVE_COMMENT, data=data)

    def _query_next_live(self, room_id):
        """Gets room's next live schedule."""
        params = {
            'room_id': room_id,
            '_': int(time.time())
        }
        return self.connections_manager.get(self.API_NEXT_LIVE, params=params)

    def _query_summary_ranking(self, room):
        """Gets summary ranking from room."""
        params = {
            'room_id': room.room_id,
            '_': int(time.time())
        }
        return self.connections_manager.get(self.API_SUMMARY_RANKING, params=params)

    def _query_settings(self, room):
        """Gets the rooms' settings."""
        params = {
            'room_id': room.room_id,
            '_': int(time.time())
        }
        return self.connections_manager.get(self.API_SETTINGS, params=params)

    def _query_stage_user_list(self, room):
        """Gets the stage user list."""
        params = {
            'room_id': room.room_id,
            '_': int(time.time())
        }
        return self.connections_manager.get(self.API_STAGE_USER_LIST, params=params)

    def _query_stage_user_list_anteroom(self, room):
        """Gets the anteroom user list."""
        params = {
            'room_id': room.room_id,
            '_': int(time.time())
        }
        return self.connections_manager.get(self.API_ANTEROOM_STAGE_USER_LIST, params=params)

    def _query_stage_gift_list(self, room):
        """Gets the stage gift list from room."""
        params = {
            'room_id': room.room_id,
            '_': int(time.time())
        }
        return self.connections_manager.get(self.API_SUMMARY_RANKING, params=params)

    def _query_enquete_result(self, room):
        """Get questionnaire result."""
        params = {
            'room_id': room.room_id,
            '_': int(time.time())
        }
        return self.connections_manager.get(self.API_ENQUETE_RESULT, params=params)

    def _query_gift_list(self, room):
        """Gets the gift list."""
        params = {
            'room_id': room.room_id,
            '_': int(time.time())
        }
        return self.connections_manager.get(self.API_GIFT_LIST, params=params)

    def _query_gifting_free(self, live, gift_id, num):
        """Throw gift in given live."""
        data = {
            'gift_id': gift_id,
            'live_id': live.live_id,
            'num': num,
            'csrf_token': self._query_csrf_token(),
            'isRemovable': True
        }
        return self.connections_manager.post(self.API_GIFTING_FREE, data=data)

    def _query_gifting_point_use(self, live, gift_id, num):
        """Throw paid gift in given live."""
        data = {
            'gift_id': gift_id,
            'live_id': live.live_id,
            'num': num,
            'csrf_token': self._query_csrf_token()
        }
        return self.connections_manager.post(self.API_GIFTING_POINT_USE, data=data)

    def _query_telop(self, room):
        """Get telop from room."""
        params = {
            'room_id': room.room_id,
            '_': int(time.time())
        }
        return self.connections_manager.get(self.API_TELOP, params=params)

    def _query_questionnaire_result(self, room):
        """Gets the questionnaire result."""
        params = {
            'room_id': room.room_id,
            '_': int(time.time())
        }
        return self.connections_manager.get(self.API_ENQUETE_RESULT, params=params)

    def _query_gift_log(self, room):
        """Gets gift log from room."""
        params = {
            'room_id': room.room_id,
            '_': int(time.time())
        }
        return self.connections_manager.get(self.API_GIFT_LOG, params=params)

    def _query_comment_log(self, room):
        """Gets comment log from room."""
        params = {
            'room_id': room.room_id,
            '_': int(time.time())
        }
        return self.connections_manager.get(self.API_COMMENT_LOG, params=params)

    def _query_tweet(self, room, comment):
        """Sends a tweet from the current room."""
        data = {
            'live_id': room.live.live_id,
            'twitter_text': comment,
            'csrf_token': self._query_csrf_token()
        }

        return self.connections_manager.post(self.API_POST_TWEET, data=data)

    def _query_login(self, username, password):
        """Logins."""
        files = OrderedDict()
        files["csrf_token"] = (None, self._query_csrf_token())
        files["account_id"] = (None, username)
        files["password"] = (None, password)
        files["captcha_word"] = (None, "")

        return self.connections_manager.post(self.API_LOGIN, files=files)

    def _query_logout(self):
        """Logout."""
        data = {
            'csrf_token': self._query_csrf_token()
        }

        return self.connections_manager.post(self.API_LOGOUT, data=data)

    def _query_tracker(self):
        """Login form."""
        data = {
            't': 'login_form',
            'csrf_token': self._query_csrf_token()
        }
        return self.connections_manager.post(self.API_TRACKER_LOG, data=data)

    def _query_update_user_avatar(self, avatar_id):
        """Updates avatar."""
        data = {
            'avatar_id': avatar_id,
            'csrf_token' : self._query_csrf_token()
        }
        return self.connections_manager.post(self.API_UPDATE_USER_AVATAR, data=data)

    def _query_profile(self, profile_configuration):
        """Updates the profile."""
        files = {}
        files["csrf_token"] = (None, self._query_csrf_token())

        if profile_configuration.name is not None:
            files["name"] = (None, profile_configuration.name)

        if profile_configuration.trim_left is not None:
            files["trim_left"] = (None, profile_configuration.trim_left)

        if profile_configuration.trim_top is not None:
            files["trim_top"] = (None, profile_configuration.trim_top)

        if profile_configuration.trim_right is not None:
            files["trim_right"] = (None, profile_configuration.trim_right)

        if profile_configuration.trim_bottom is not None:
            files["trim_bottom"] = (None, profile_configuration.trim_bottom)

        if profile_configuration.trim_width is not None:
            files["trim_width"] = (None, profile_configuration.trim_width)

        if profile_configuration.trim_height is not None:
            files["trim_height"] = (None, profile_configuration.trim_height)

        if profile_configuration.trim_origin_width is not None:
            files["trim_origin_width"] = (None, profile_configuration.trim_origin_width)

        if profile_configuration.trim_origin_height is not None:
            files["trim_origin_height"] = (None, profile_configuration.trim_origin_height)

        if profile_configuration.profile_image is not None:
            files["profile_image"] = (None, "", 'application/octet-stream')

        if profile_configuration.avatar_id is not None:
            files["avatar_id"] = (None, str(profile_configuration.avatar_id))

        if profile_configuration.description is not None:
            files["description"] = (None, profile_configuration.description)

        return self.connections_manager.post(self.API_PROFILE_EDIT, files=files)

    def _query_room_profile(self, room):
        """Gets room information."""
        params = {
            'room_id': room.room_id,
            '_': int(time.time())
        }
        return self.connections_manager.get(self.API_ROOM_PROFILE, params=params)
