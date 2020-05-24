"""Daemon configuration parser."""
from srtools.utils.commandline.base import IConfigurationInterface

class Daemon(IConfigurationInterface):
    """Daemon parser."""
    def __init__(self, configuration, parser):
        """Constructor for the List option."""
        IConfigurationInterface.__init__(self, configuration, parser)

    def setup(self, subparsers):
        """Setups the parser for the Daemon option."""
        parser = subparsers.add_parser('daemon')
        parser.add_argument('')
        return parser

    def parse(self, args):
        """Daemon items."""
