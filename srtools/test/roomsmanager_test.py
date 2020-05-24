"""Unit tests for GenresManager."""
from srtools.test.showroommanager_test import ShowroomManagerTest
from srtools.manager.roomsmanager import RoomsManager

class ShowroomManagerRooms(ShowroomManagerTest):
    """ShowroomFakeManagerRooms."""
    @classmethod
    def setUpClass(cls):
        super(ShowroomManagerRooms, cls).setUpClass()

    def setUp(self):
        super(ShowroomManagerRooms, self).setUp()

    def test_rooms_load(self):
        """test_rooms_load."""
        rooms = self.showroom_manager_fake.rooms_manager.rooms()
        self.assertIsNotNone(rooms)
        self.assertEqual(108, len(rooms))

    def test_create_filter(self):
        """test_create_filter."""
        rooms_filter = self.showroom_manager.rooms_manager.create_filter()
        self.assertIsNotNone(rooms_filter)
        self.assertIsNone(rooms_filter.live)
        self.assertIsNone(rooms_filter.room_id)
        self.assertIsNone(rooms_filter.room_url_key)
        self.assertIsNone(rooms_filter.genre)
        self.assertIsNone(rooms_filter.avatar_id)
        self.assertIsNone(rooms_filter.has_upcoming)
        self.assertIsNone(rooms_filter.badge)
        self.assertIsNone(rooms_filter.image)
        self.assertIsNone(rooms_filter.avatar_url)
        self.assertIsNone(rooms_filter.telop)
        self.assertIsNone(rooms_filter.official)
        self.assertIsNone(rooms_filter.bonus_checked)
        self.assertIsNone(rooms_filter.tweet_default)
        self.assertEqual(RoomsManager.RoomsSort.UNDEFINED, rooms_filter.order_by)

    def test_rooms_filter_room_id_asc(self):
        """test_rooms_filter."""
        rooms_filter = self.showroom_manager.rooms_manager.create_filter()
        rooms_filter.order_by = RoomsManager.RoomsSort.ROOM_ID_ASC
        rooms = self.showroom_manager.rooms_manager.rooms(rooms_filter)

        total = len(rooms)
        index = 0
        while index < total - 1:
            self.assertGreater(rooms[index + 1].room_id, rooms[index].room_id)
            index += 1

    def test_rooms_filter_room_id_desc(self):
        """test_rooms_filter."""
        rooms_filter = self.showroom_manager.rooms_manager.create_filter()
        rooms_filter.order_by = RoomsManager.RoomsSort.ROOM_ID_DESC
        rooms = self.showroom_manager.rooms_manager.rooms(rooms_filter)

        total = len(rooms)
        index = 0
        while index < total - 1:
            self.assertGreater(rooms[index].room_id, rooms[index + 1].room_id)
            index += 1

    def test_rooms_filter_live_id_asc(self):
        """test_rooms_filter."""
        rooms_filter = self.showroom_manager.rooms_manager.create_filter()
        rooms_filter.order_by = RoomsManager.RoomsSort.LIVE_ID_ASC
        rooms = self.showroom_manager.rooms_manager.rooms(rooms_filter)

        total = len(rooms)
        index = 0
        while index < total - 1:
            self.assertGreater(rooms[index + 1].live.live_id, rooms[index].live.live_id)
            index += 1

    def test_rooms_filter_live_id_desc(self):
        """test_rooms_filter."""
        rooms_filter = self.showroom_manager.rooms_manager.create_filter()
        rooms_filter.order_by = RoomsManager.RoomsSort.LIVE_ID_DESC
        rooms = self.showroom_manager.rooms_manager.rooms(rooms_filter)

        total = len(rooms)
        index = 0
        while index < total - 1:
            self.assertGreater(rooms[index].live.live_id, rooms[index + 1].live.live_id)
            index += 1

    def test_send_multiple_comments(self):
        """Unit test for commenting."""
        rooms_filter = self.showroom_manager.rooms_manager.create_filter()
        rooms_filter.order_by = RoomsManager.RoomsSort.LIVE_ID_DESC
        rooms = self.showroom_manager.rooms_manager.rooms(rooms_filter)

        room = rooms[0]
        for comment in range(1, 7):
            respjson = self.showroom_manager.showroom_api.send_comment(room.live, comment)
            self.assertIsNotNone(respjson)

    def test_next_live(self):
        """Unit test for next live."""

    def test_room_to_string(self):
        """Unit test for __str__."""
        room = self.showroom_manager_fake.rooms_manager.find(97446)
        result = str(room)
        self.assertEqual("97446", result)
