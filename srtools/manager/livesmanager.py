"""Live information."""
from srtools.manager.basemanager import BaseManager

class LivesManager(BaseManager):
    """Showroom lives manager."""

    class Live(object):
        """Showroom live information."""
        def __init__(self, live_id):
            self.json = None
            self.new_streaming = None
            self.broadcast_port = None
            self.live_user_key = None
            self.is_twitter_auth = None
            self.service_setting = None
            self.broadcast_key = None
            self.get_daily_bonus = None
            self.upload_url_bak = None
            self.is_login = None
            self.upload_url_hls = None
            self.upload_url = None
            self.support_users = None
            self.rtmp_proxy_url = None
            self.upload_url_ams = None
            self.streaming_url_rtmp = None
            self.is_live = None
            self.origin_key = None
            self.daily_bonus_item_id = None
            self.streaming_name_rtmp = None
            self.tweet_default = ''
            self.regular_event_data = None
            self.streaming_key = None
            self.streaming_url_list = None
            self.event_data = None
            self.upload_url_gip = None
            self.ranking = None
            self.live_res = None
            self.room_id = None
            self.has_event = None
            self.modal_dialog_url_for_app = None
            self.background_image_url = None
            self.has_regular_event = None
            self.streaming_url_list_rtmp = None
            self.has_support = None
            self.tweet_url = None
            self.broadcast_host = None
            self.telop = None
            self.room = None
            self.is_enabled_full_screen = None
            self.is_owner = None
            self.streaming_url_hls = None
            self.online_user_num = None
            self.gift_html = None
            self.upload_url_ams_bak = None
            self.is_enquete = None
            self.gift_list = None
            self.nsta_owner = None
            self.high_point_gift_list = None
            self.enquete_data = None
            self.live_id = live_id
            self.my_data = None
            self.support_data = None

        def __str__(self):
            return str(self.live_id)

    def __init__(self, configuration, showroom_api):
        super(LivesManager, self).__init__(configuration, showroom_api)
        self.lives = {}

    def create(self, live_id):
        """Creates and returns a live event."""
        self.lives[live_id] = self.Live(live_id)
        return self.lives[live_id]

    def find(self, live_id):
        """Finds and returns the requested self."""
        if live_id in self.lives:
            result = self.lives[live_id]
        else:
            result = None

        return result

    def refresh(self, live, livejson):
        """Refreshes live information."""
        live.json = livejson
        live.new_streaming = livejson.get('new_streaming')
        live.broadcast_port = livejson.get('bcsvr_port')
        live.live_user_key = livejson.get('live_user_key')
        live.is_twitter_auth = livejson.get('is_twitter_auth')
        live.service_setting = livejson.get('service_setting')
        live.broadcast_key = livejson.get('bcsvr_key')
        live.get_daily_bonus = livejson.get('get_daily_bonus')
        live.upload_url_bak = livejson.get('upload_url_bak')
        live.is_login = livejson.get('is_login')
        live.upload_url_hls = livejson.get('upload_url_hls')
        live.upload_url = livejson.get('upload_url')
        live.support_users = livejson.get('support_users')
        live.rtmp_proxy_url = livejson.get('rtmp_proxy_url')
        live.upload_url_ams = livejson.get('upload_url_ams')
        live.streaming_url_rtmp = livejson.get('streaming_url_rtmp')
        live.is_live = livejson.get('is_live')
        live.origin_key = livejson.get('origin_key')
        live.daily_bonus_item_id = livejson.get('daily_bonus_item_id')
        live.streaming_name_rtmp = livejson.get('streaming_name_rtmp')
        live.room = livejson.get('room')
        live.tweet_default = livejson.get('tweet_default')
        if live.tweet_default is None:
            if live.room is not None:
                live.tweet_default = ("%s broadcasting!" % live.room.get('room_name'))
            else:
                live.tweet_default = "Default"
        live.regular_event_data = livejson.get('regular_event_data')
        live.streaming_key = livejson.get('streaming_key')
        live.streaming_url_list = livejson.get('streaming_url_list')
        live.event_data = livejson.get('event_data')
        live.upload_url_gip = livejson.get('upload_url_gip')
        live.ranking = livejson.get('ranking')
        live.live_res = livejson.get('live_res')
        live.room_id = livejson.get('room_id')
        live.has_event = livejson.get('has_event')
        live.modal_dialog_url_for_app = livejson.get('modal_dialog_url_for_app')
        live.background_image_url = livejson.get('background_image_url')
        live.has_regular_event = livejson.get('has_regular_event')
        live.streaming_url_list_rtmp = livejson.get('streaming_url_list_rtmp')
        live.has_support = livejson.get('has_support')
        live.tweet_url = livejson.get('tweet_url')
        live.broadcast_host = livejson.get('bcsvr_host')
        live.telop = livejson.get('telop')
        live.is_enabled_full_screen = livejson.get('is_enabled_full_screen')
        live.is_owner = livejson.get('is_owner')
        live.streaming_url_hls = livejson.get('streaming_url_hls')
        live.online_user_num = livejson.get('online_user_num')
        live.gift_html = livejson.get('gift_html')
        live.upload_url_ams_bak = livejson.get('upload_url_ams_bak')
        live.is_enquete = livejson.get('is_enquete')
        live.gift_list = livejson.get('gift_list')
        live.nsta_owner = livejson.get('nsta_owner')
        live.high_point_gift_list = livejson.get('high_point_gift_list')
        live.enquete_data = livejson.get('enquete_data')
        live.live_id = livejson.get('live_id')
        live.my_data = livejson.get('my_data')
        live.support_data = livejson.get('support_data')
