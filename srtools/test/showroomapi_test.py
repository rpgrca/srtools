"""Unit tests for ShowroomAPI."""
import unittest
from srtools.manager.api.showroomapi import ShowroomAPI
from srtools.configuration.configuration import Configuration

class ShowroomAPITest(unittest.TestCase):
    """Base for ShowroomAPI unit test fixture."""
    def setUp(self):
        self.configuration = Configuration()
        self.configuration.connection.cookies = "chrome"
        self.showroom_api = ShowroomAPI(self.configuration)

    def tearDown(self):
        pass

class ShowroomAPIOnlivesTest(ShowroomAPITest):
    """ShowroomAPI unit test"""

    def test_get_onlive_num(self):
        """Unit test for get_onlive_num."""
        value = self.showroom_api.get_onlive_num()
        self.assertIsNotNone(value)
        self.assertGreaterEqual(value, 0)

    def test_get_onlives(self):
        """Unit test for query_onlives."""
        respjson = self.showroom_api.get_onlives()
        self.assertIsNotNone(respjson)
        self.assertEqual(8, len(respjson.get('onlives')))

    def test_refresh_token(self):
        """Unit test for refresh token."""
        #self.showroom_api.refresh_token()

    def test_profile_update(self):
        """Unit test for profile update."""
        values = [
            {'name': None, 'avatar_id': None, 'result': False},
            {'name': 'test', 'avatar_id': None, 'result': False},
            {'name': None, 'avatar_id': '25', 'result': False},
            {'name': 'user', 'avatar_id': '206004', 'result': False},
            {'name': 'test', 'avatar_id': '25', 'result': True}
        ]

        for value in values:
            self.configuration.profile.name = value['name']
            self.configuration.profile.avatar_id = value['avatar_id']
            self.assertEqual(value['result'],
                             self.showroom_api.update_profile(self.configuration.profile))

    def test_login(self):
        """Unit test for login."""
        self.assertTrue(self.showroom_api.login("", ""))

if __name__ == '__main__':
    unittest.main()
