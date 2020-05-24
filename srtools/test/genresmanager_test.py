"""Unit tests for GenresManager."""
import uuid
import random
#import unittest
from srtools.test.showroommanager_test import ShowroomManagerTest

class ShowroomManagerGenres(ShowroomManagerTest):
    """ShowroomManagerGenres."""
    def setUp(self):
        super(ShowroomManagerGenres, self).setUp()
        self.genres = [{'genre_id': 0, 'genre_name': u'Popularity'},
                       {'genre_id': 101, 'genre_name': u'Music'},
                       {'genre_id': 102, 'genre_name': u'Idol'},
                       {'genre_id': 103, 'genre_name': u'Talent Model'},
                       {'genre_id': 104, 'genre_name': u'Voice Actors & Anime'},
                       {'genre_id': 105, 'genre_name': u'Comedians/Talk Show'},
                       {'genre_id': 106, 'genre_name': u'Sports'},
                       {'genre_id': 200, 'genre_name': u'Non-Professionals'}]

    def _test_filter(self, genre_id, genre_name):
        """filter."""
        genres = [{'genre_id': genre_id, 'genre_name': None},
                  {'genre_id': None, 'genre_name': genre_name},
                  {'genre_id': genre_id, 'genre_name': genre_name}]

        for genre in genres:
            genre_filter = self.showroom_manager.genres_manager.create_filter()
            genre_filter.genre_id = genre['genre_id']
            genre_filter.genre_name = genre['genre_name']
            hit = self.showroom_manager.genres_manager.genres(genre_filter)
            self.assertIsNotNone(hit)
            self.assertEqual(1, len(hit))
            self.assertEqual(genre_id, hit[0].genre_id)
            self.assertEqual(genre_name, hit[0].genre_name)

    def test_create_filter(self):
        """test_create_filter."""
        genre_filter = self.showroom_manager.genres_manager.create_filter()
        self.assertIsNotNone(genre_filter)
        self.assertIsNone(genre_filter.genre_id)
        self.assertIsNone(genre_filter.genre_name)

    def test_genre_list(self):
        """test_fake_load."""

        genres = self.showroom_manager.genres_manager.genres()
        self.assertEqual(len(self.genres), len([x for x in genres if x.genre_id <= 200]))

        for genre in genres:
            self.assertIsNotNone([x for x in self.genres \
                                 if x['genre_id'] == genre.genre_id and \
                                 x['genre_name'] == genre.genre_name])
            value = "{'genre_name': u'%s', 'genre_id': %s}" % (genre.genre_name, genre.genre_id)
            self.assertEquals(value, str(genre))

    def test_genre_list_empty(self):
        """test_genre_list_empty."""

        genre_filter = self.showroom_manager.genres_manager.create_filter()
        genre_filter.genre_id = random.randint(2000, 2500)
        genre_filter.genre_name = str(uuid.uuid4())
        genres = self.showroom_manager.genres_manager.genres(genre_filter)
        self.assertIsNotNone(genres)

    def test_genre_filter(self):
        """test_filter."""

        for genre in self.genres:
            self._test_filter(genre['genre_id'], genre['genre_name'])

    def test_genre_create(self):
        """test_genre_create."""
        genre_id = random.randint(2000, 2500)
        genre_name = str(uuid.uuid4())
        length = 0

        genres1 = self.showroom_manager.genres_manager.genres()
        length = len(genres1)

        self.showroom_manager.genres_manager.create(genre_id, genre_name)
        genres2 = self.showroom_manager.genres_manager.genres()
        self.assertEqual(length + 1, len(genres2))
        self._test_filter(genre_id, genre_name)

        genres3 = self.showroom_manager.genres_manager.genres()
        self.assertEqual(length + 1, len(genres3))

    def test_genre_create_duplicate(self):
        """test_genre_create_duplicate."""
        genre_id = random.randint(2000, 2500)
        genre_name = str(uuid.uuid4())
        length = 0

        genres1 = self.showroom_manager.genres_manager.genres()
        length = len(genres1)
        genre = self.showroom_manager.genres_manager.create(genre_id, genre_name)
        genres2 = self.showroom_manager.genres_manager.genres()
        self.assertEqual(length + 1, len(genres2))

        genre2 = self.showroom_manager.genres_manager.create(genre_id, genre_name)
        self.assertEquals(genre.genre_id, genre2.genre_id)
        self.assertEquals(genre.genre_name, genre2.genre_name)
