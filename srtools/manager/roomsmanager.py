"""Rooms Manager"""
from enum import Enum

from srtools.manager.basemanager import BaseManager

class RoomsManager(BaseManager):
    """Showroom Rooms Manager."""
    class RoomsSort(Enum):
        """Sort rooms."""
        UNDEFINED = 0
        ROOM_ID_ASC = 1
        ROOM_ID_DESC = 2
        GENRES_ASC = 3
        GENRES_DESC = 4
        LIVE_ID_ASC = 5
        LIVE_ID_DESC = 6

    class Room(object):
        """Showroom room information."""
        def __init__(self, room_id):
            self.live = None
            self.room_id = room_id
            self.room_url_key = None
            self.genres = []
            self.avatars = []
            self.avatars_checked = False
            self.has_upcoming = False
            self.badge = False
            self.image = None
            self.avatar_url = None
            self.telop = None
            self.official = None
            self.bonus_checked = False
            self.tweet_default = ""

        def __str__(self):
            """"""
            return str(self.room_id)

    class RoomsFilter(object):
        """Showroom rooms filter information."""
        def __init__(self):
            self.live = None
            self.room_id = None
            self.room_url_key = None
            self.genre = None
            self.avatar_id = None
            self.has_upcoming = None
            self.badge = None
            self.image = None
            self.avatar_url = None
            self.telop = None
            self.official = None
            self.bonus_checked = None
            self.tweet_default = None
            self.order_by = RoomsManager.RoomsSort.UNDEFINED

    def __init__(self, configuration, showroom_api):
        super(RoomsManager, self).__init__(configuration, showroom_api)
        self._rooms = {}

    def create(self, room_id):
        """Creates and returns a room."""
        self._rooms[room_id] = self.Room(room_id)
        return self._rooms[room_id]

    def create_filter(self):
        """Creates and returns a room filter."""
        return self.RoomsFilter()

    def find(self, room_id):
        """Returns the requested room information."""
        if self.contains(room_id):
            result = self._rooms[room_id]
        else:
            result = None

        return result

    def contains(self, room_id):
        """Returns whether the room exists internally."""
        return room_id in self._rooms

    def rooms(self, rooms_filter=None):
        """Returns a list of rooms."""

        if rooms_filter is None:
            rooms_filter = self.RoomsFilter()

        rooms = [x for x in self._rooms.values() \
                if (rooms_filter.live is None or (x.live is not None and x.live.live_id == rooms_filter.live.live_id)) and \
                   (rooms_filter.room_id is None or rooms_filter.room_id < 1 or (x.room_id == rooms_filter.room_id)) and \
                   (rooms_filter.room_url_key is None or (x.room_url_key == rooms_filter.room_url_key)) and \
                   (rooms_filter.avatar_id is None or (x.avatar_id == rooms_filter.avatar_id)) and \
                   (rooms_filter.has_upcoming is None or (x.has_upcoming == rooms_filter.has_upcoming)) and \
                   (rooms_filter.badge is None or (x.badge == rooms_filter.badge)) and \
                   (rooms_filter.image is None or (x.image == rooms_filter.image)) and \
                   (rooms_filter.avatar_url is None or (x.avatar_url == rooms_filter.avatar_url)) and \
                   (rooms_filter.telop is None or (x.telop == rooms_filter.telop)) and \
                   (rooms_filter.official is None or (x.official == rooms_filter.official)) and \
                   (rooms_filter.bonus_checked is None or (x.bonus_checked == rooms_filter.bonus_checked)) and \
                   (rooms_filter.tweet_default is None or (x.tweet_default == rooms_filter.tweet_default)) and \
                   (rooms_filter.genre is None or (x.genres is not None and rooms_filter.genre in x.genres))]

        if rooms_filter.order_by == RoomsManager.RoomsSort.LIVE_ID_ASC:
            rooms = sorted([x for x in rooms if x.live is not None], key=lambda x: x.live.live_id)
        elif rooms_filter.order_by == RoomsManager.RoomsSort.LIVE_ID_DESC:
            rooms = sorted([x for x in rooms if x.live is not None], key=lambda x: x.live.live_id, reverse=True)
        elif rooms_filter.order_by == RoomsManager.RoomsSort.ROOM_ID_ASC:
            rooms = sorted(rooms, key=lambda x: x.room_id)
        elif rooms_filter.order_by == RoomsManager.RoomsSort.ROOM_ID_DESC:
            rooms = sorted(rooms, key=lambda x: x.room_id, reverse=True)

        return rooms
