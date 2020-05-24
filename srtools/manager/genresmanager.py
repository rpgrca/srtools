"""Genres Manager"""
from srtools.manager.basemanager import BaseManager

class GenresManager(BaseManager):
    """Showroom Genres Manager."""

    class Genre(object):
        """Showroom genre information."""
        def __init__(self, genre_id, genre_name):
            self.genre_id = genre_id
            self.genre_name = genre_name

        def __str__(self):
            return str(vars(self))

    class GenresFilter(object):
        """Showroom genre filter."""
        def __init__(self):
            self.genre_id = None
            self.genre_name = None

    def __init__(self, configuration, showroom_api):
        super(GenresManager, self).__init__(configuration, showroom_api)
        self._genres = {}

    def create(self, genre_id, genre_name):
        """Creates and returns a new genre with the given information"""
        self._genres[genre_id] = self.Genre(genre_id, genre_name)
        return self._genres[genre_id]

    def create_filter(self):
        """Returns a genre filter."""
        return self.GenresFilter()

    def find(self, genre_id):
        """Returns the requested genre information"""
        if genre_id in self._genres:
            result = self._genres[genre_id]
        else:
            result = None

        return result

    def genres(self, genres_filter=None):
        """Returns a list of genres matching the requirements"""
        if genres_filter is None:
            genres_filter = self.GenresFilter()

        return [x for x in self._genres.values() \
                if (genres_filter.genre_id is None or (x.genre_id == genres_filter.genre_id)) and \
                (genres_filter.genre_name is None or (x.genre_name == genres_filter.genre_name))]
