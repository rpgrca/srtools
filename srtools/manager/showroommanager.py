"""Main manager."""
from srtools.manager.livesmanager import LivesManager
from srtools.manager.roomsmanager import RoomsManager
from srtools.manager.genresmanager import GenresManager
from srtools.manager.api.showroomapi import ShowroomAPI
from srtools.utils.loggingutils import log_error

class ShowroomManager(object):
    """Manager group."""
    def __init__(self, configuration, showroom_api=None):
        self.configuration = configuration
        self.showroom_api = showroom_api \
                            if showroom_api is not None else ShowroomAPI(self.configuration)
        self.lives_manager = None
        self.rooms_manager = None
        self.genres_manager = None
        self.initialize()

    def _create_managers(self):
        """Create internal managers."""
        self.lives_manager = LivesManager(self.configuration, self.showroom_api)
        self.rooms_manager = RoomsManager(self.configuration, self.showroom_api)
        self.genres_manager = GenresManager(self.configuration, self.showroom_api)

    def initialize(self):
        """Initializes the managers."""
        self._create_managers()
        try:
            respjson = self.showroom_api.get_onlives()
            if respjson is not None:
                for genre in respjson['onlives']:
                    current_genre = self.genres_manager.find(genre['genre_id'])
                    if current_genre is None:
                        current_genre = self.genres_manager.create(genre['genre_id'],
                                                                   genre['genre_name'])

                    for room in genre['lives']:
                        if room.get('room_id') is not None:
                            current_room = self.rooms_manager.find(room['room_id'])
                            if current_room is None:
                                current_room = self.rooms_manager.create(room['room_id'])
                                current_room.cell_type = room['cell_type']
                                current_room.follower_num = room['follower_num']
                                current_room.is_follow = room['is_follow']
                                current_room.image = room['image']
                                current_room.tags = room['tags']
                                current_room.live_type = room['live_type']
                                current_room.view_num = room['view_num']
                                current_room.room_url_key = room['room_url_key']
                                current_room.name = room['main_name']
                                current_room.official = room['official_lv']
                                current_room.bcsvr_key = room['bcsvr_key']
                                current_room.started_at = room['started_at']
                                current_room.main_name = room['main_name']
                                current_room.bonus_checked = False
                                current_room.badge = False
                                current_room.live = self.lives_manager.create(room['live_id'])
                                current_room.genre = current_genre
                            else:
                                if current_room.live.live_id != room['live_id']:
                                    current_room.live = self.lives_manager.create(room['live_id'])

        except StandardError as err:
            log_error(err)
