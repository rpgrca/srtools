"""List configuration parser."""
from srtools.configuration.configuration import SelectedConfiguration
from srtools.utils.commandline.connection import Connection

class Lottery(Connection):
    """List parser."""
    def __init__(self, configuration, parser):
        """Constructor for the Lottery option."""
        super(Lottery, self).__init__(configuration, parser)

    def setup(self, subparsers):
        """Setups the parser for the Lottery option."""
        parent = super(Lottery, self).setup(subparsers)
        parser = subparsers.add_parser('lottery', parents=[parent])
        parser.add_argument('name', help='lottery name')
        parser.add_argument('-t', '--target', help='target avatar (0: none)', type=int,
                            default=self.configuration.lottery.target)
        parser.set_defaults(func=self.parse)
        return parser

    def parse(self, args):
        """Lottery items."""
        super(Lottery, self).parse(args)
        self.configuration.chosen = SelectedConfiguration.LOTTERY
        self.configuration.lottery.name = args.name
        self.configuration.lottery.target = args.target
