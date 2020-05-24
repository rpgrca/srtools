"""Base for configuration parser."""
from abc import ABCMeta, abstractmethod
from srtools.configuration.configuration import SelectedConfiguration
from srtools.configuration.configuration import FreeGifts, BallotGifts, PaidGifts

class IConfigurationInterface(object):
    """Base configuration class"""
    __metaclass__ = ABCMeta

    configuration = None
    parser = None

    def __init__(self, configuration, parser):
        """Constructor."""
        self.configuration = configuration
        self.parser = parser

    @classmethod
    def version(cls):
        """Returns current version."""
        return "1.0"

    @abstractmethod
    def setup(self, subparsers):
        """Interface for setting up the parser."""
        raise NotImplementedError

    @abstractmethod
    def parse(self, args):
        """Fills parse object."""
        raise NotImplementedError

    def _convert_group(self, group):
        """Converts a group nickname into room ids."""
        values = []

        try:
            if ',' in group:
                elements = group.split(',')
            else:
                elements = [group]

            for element in elements:
                if element in self.configuration.favorite_groups:
                    values += self.configuration.favorite_groups[element]
                elif element in self.configuration.hunted_avatars:
                    values += self.configuration.hunted_avatars[element]
                else:
                    values.append(self._convert_room(element))

                #else:
                    #values = [x for x in group.split(',')]
        except StandardError as _err:
            self.parser.error("Unknown group alias (%s)" % group)

        return values

    def _convert_room(self, room):
        """Converts a room nickname into room id."""
        value = 0

        try:
            value = int(room)
        except ValueError:
            if room in self.configuration.favorite_users:
                value = self.configuration.favorite_users[room]
            elif room == 'list':
                self.configuration.chosen = SelectedConfiguration.LIST_USERS
            else:
                self.parser.error("Unknown room alias (%s)" % room)

        return value

    def _convert_avatar(self, avatar):
        """Converts an avatar nickname into avatar id."""
        value = 0

        try:
            value = int(avatar)
        except ValueError:
            if avatar in self.configuration.favorite_avatars:
                value = self.configuration.favorite_avatars[avatar]
            elif avatar == 'list':
                self.configuration.chosen = SelectedConfiguration.LIST_AVATARS
            else:
                self.parser.error("Unknown avatar alias (%s)" % avatar)

        return value

    @staticmethod
    def _parse_items(string):
        """Parse command line item list."""
        gifts = {}

        for i in FreeGifts:
            gifts[i.name] = i.value

        for i in BallotGifts:
            gifts[i.name] = i.value

        for i in PaidGifts:
            gifts[i.name] = i.value

        result = [{u'free_num': int(x.split('=')[1]), u'gift_id': gifts[x.split('=')[0]]}
                  for x in string.split(',')]

        return result
