"""Unit tests for Broadcast callbacks."""
import io
import unittest
from srtools.manager.api.callbacks.defaultbroadcastcallback import DefaultBroadcastCallback
from srtools.configuration.configuration import Configuration
from srtools.manager.api.showroombroadcast import ShowroomBroadcast
from srtools.manager.roomsmanager import RoomsManager
from srtools.manager.livesmanager import LivesManager

class FakeShowroomBroadcast(ShowroomBroadcast):
    """Fake Showroom Broadcast."""
    def __init__(self, configuration, room, user):
        super(FakeShowroomBroadcast, self).__init__(configuration, room, user)
        #inputfile = codecs.open('akb48_senkyo_new.txt', encoding='ascii)
        #self.message_list = inputfile.readlines()
        with io.open("../ac_error.txt", "r", encoding="utf-8") as inputfile:
            self.message_list = ['\t'.join(x[:-1].split('\t')[1:]) \
                                 if x[-1] == '\n' else \
                                 '\t'.join(x.split('\t')[1:]) for x in inputfile.readlines()]

    def _send_message(self, message):
        pass

    def _connect(self, address, port):
        pass

    def _do_ping(self):
        pass

    def _receive(self):
        iterator = iter(self.message_list)
        self.message_list = ['MSG	1f913d:hIznds0a	{"created_at":1499581304,"n":0,"a":"214063","t":101}']
        return iterator

class BroadcastCallbackTest(unittest.TestCase):
    """Base for ShowroomAPI unit test fixture."""
    def setUp(self):
        self.configuration = Configuration()

    def tearDown(self):
        pass

    def test_utf8(self):
        """Test UTF-8."""
        room = RoomsManager(self.configuration, None).create("1")
        room.live = LivesManager(self.configuration, None).create("1")

        broadcast = FakeShowroomBroadcast(self.configuration, room, None)
        broadcast.do_communication(DefaultBroadcastCallback(self.configuration, room))
