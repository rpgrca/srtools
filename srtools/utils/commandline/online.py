"""Online configuration parser."""
from srtools.configuration.configuration import SelectedConfiguration
from srtools.utils.commandline.base import IConfigurationInterface

class Online(IConfigurationInterface):
    """Online parser."""
    def __init__(self, configuration, parser):
        """Constructor for the Online option."""
        super(Online, self).__init__(configuration, parser)

    def setup(self, subparsers):
        """Setups the parser for the Online option."""
        parser = subparsers.add_parser('online')
        parser.add_argument('target_room', help='target room id or shortcut',
                            type=self._convert_room)
        parser.add_argument('-v', '--verbose', help='verbose result (default: %s)' %
                            self.configuration.online.verbose, action='store_true',
                            default=self.configuration.online.verbose)
        parser.set_defaults(func=self.parse)
        return parser

    def parse(self, args):
        """Online items."""
        if self.configuration.chosen == SelectedConfiguration.UNDEFINED:
            self.configuration.chosen = SelectedConfiguration.ONLINE
            self.configuration.online.target_room = args.target_room
            self.configuration.online.verbose = args.verbose
