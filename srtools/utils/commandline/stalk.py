"""Stalk configuration parser."""
from srtools.configuration.configuration import SelectedConfiguration
from srtools.utils.commandline.connection import Connection

class Stalk(Connection):
    """Track parser."""
    def __init__(self, configuration, parser):
        """Constructor for the Hunt option."""
        super(Stalk, self).__init__(configuration, parser)

    def setup(self, subparsers):
        """Setups the parser for the Hunt option."""
        parent = super(Stalk, self).setup(subparsers)
        parser = subparsers.add_parser('stalk', parents=[parent])
        parser.add_argument('-r', '--rooms', help='list of rooms to stalk', nargs="+",
                            type=self._convert_group, default=self.configuration.stalk.target_rooms)
        parser.add_argument('-d', '--delay', type=int, default=self.configuration.stalk.delay,
                            help='delay between stalk check (default: %s seconds)' %
                            self.configuration.stalk.delay)
        parser.add_argument('-s', '--simulate', default=self.configuration.stalk.simulate,
                            help='run simulation (no item throwing, default: %s)' %
                            self.configuration.stalk.simulate, action='store_true')
        parser.add_argument('-t', '--target-file', help='target log file (default: %s)' %
                            self.configuration.stalk.target_file,
                            default=self.configuration.stalk.target_file)
        parser.set_defaults(func=self.parse)
        return parser

    def parse(self, args):
        """Stalk items."""
        super(Stalk, self).parse(args)
        self.configuration.chosen = SelectedConfiguration.STALK
        self.configuration.stalk.delay = args.delay
        self.configuration.stalk.target_file = args.target_file
        self.configuration.stalk.simulate = args.simulate
        self.configuration.stalk.target_rooms = []
        if args.rooms and len(args.rooms) > 0:
            for sublist in args.rooms:
                if isinstance(sublist, list):
                    self.configuration.stalk.target_rooms += sublist
                else:
                    self.configuration.stalk.target_rooms.append(sublist)
