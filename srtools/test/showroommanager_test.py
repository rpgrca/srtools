"""Unit tests for ShowroomManager."""
import unittest
import json
from srtools.manager.showroommanager import ShowroomManager
from srtools.manager.servicesmanager import ServicesManager
from srtools.manager.api.showroomapi import ShowroomAPI
from srtools.configuration.configuration import Configuration

class FakeShowroomAPI(ShowroomAPI):
    """FakeShowroomAPI."""
    class FakeString(object):
        """FakeString."""
        def __init__(self, text):
            self._text = text

        def json(self):
            """Returns a json object."""
            return json.loads(self._text)

    def __init__(self, configuration):
        super(FakeShowroomAPI, self).__init__(configuration)

    def get_onlives(self):
        """query_onlives."""
        json_file = open("srtools/test/resources/onlives.json", "r")
        lines = json_file.readlines()
        json_file.close()

        return self.FakeString(" ".join(lines)).json()

class ShowroomManagerTest(unittest.TestCase):
    """ShowroomManagerTest."""

    configuration = None
    showroom_manager = None
    showroom_manager_fake = None

    @classmethod
    def setUpClass(cls):
        super(ShowroomManagerTest, cls).setUpClass()
        cls.configuration = Configuration()
        cls.showroom_manager = ShowroomManager(cls.configuration)
        cls.showroom_manager_fake = ShowroomManager(cls.configuration,
                                                    FakeShowroomAPI(cls.configuration))

class ShowroomServicesTest(unittest.TestCase):
    """ShowroomServicesTest."""

    configuration = None
    showroom_services = None

    @classmethod
    def setUpClass(cls):
        super(ShowroomServicesTest, cls).setUpClass()
        cls.configuration = Configuration()
        showroom_manager = ShowroomManager(cls.configuration, ShowroomAPI(cls.configuration))
        cls.showroom_services = ServicesManager(cls.configuration, showroom_manager)

    def test_comment_log(self):
        """Unit test for log."""
        room = self.showroom_services.showroom_manager.rooms_manager.find(90487)
        self.assertIsNotNone(self.showroom_services.showroom_manager.showroom_api.get_comment_log(room))
