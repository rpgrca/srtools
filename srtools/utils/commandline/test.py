"""Test configuration parser."""
from srtools.configuration.configuration import SelectedConfiguration
from srtools.utils.commandline.base import IConfigurationInterface

class Test(IConfigurationInterface):
    """Test parser."""
    def __init__(self, configuration, parser):
        """Constructor for the Test option."""
        IConfigurationInterface.__init__(self, configuration, parser)

    def setup(self, subparsers):
        """Setups the parser for the Test option."""
        parser = subparsers.add_parser('test')
        parser.add_argument('target_room', help='target room id or shortcut')
        parser.set_defaults(func=self.parse)
        return parser

    def parse(self, args):
        """Test items."""
        self.configuration.chosen = SelectedConfiguration.TEST
        self.configuration.test.target_room = args.target_room
