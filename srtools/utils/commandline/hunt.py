"""Hunt configuration parser."""
from srtools.configuration.configuration import SelectedConfiguration
from srtools.utils.commandline.connection import Connection

class Hunt(Connection):
    """Track parser."""
    def __init__(self, configuration, parser):
        """Constructor for the Hunt option."""
        super(Hunt, self).__init__(configuration, parser)

    def setup(self, subparsers):
        """Setups the parser for the Hunt option."""
        parent = super(Hunt, self).setup(subparsers)
        parser = subparsers.add_parser('hunt', parents=[parent])
        parser.add_argument('-r', '--rooms', help='list of rooms to hunt', nargs="+",
                            type=self._convert_group, default=self.configuration.hunt.target_rooms)
        parser.add_argument('-d', '--delay', type=int, default=self.configuration.hunt.delay,
                            help='delay between hunt check (default: %s seconds)' %
                            self.configuration.hunt.delay)
        parser.add_argument('-s', '--simulate', default=self.configuration.hunt.simulate,
                            help='run simulation (no item throwing, default: %s)' %
                            self.configuration.hunt.simulate, action='store_true')
        parser.add_argument('-t', '--target-file', help='target log file (default: %s)' %
                            self.configuration.hunt.target_file,
                            default=self.configuration.hunt.target_file)
        parser.set_defaults(func=self.parse)
        return parser

    def parse(self, args):
        """Hunt items."""
        super(Hunt, self).parse(args)
        self.configuration.chosen = SelectedConfiguration.HUNT
        self.configuration.hunt.delay = args.delay
        self.configuration.hunt.target_file = args.target_file
        self.configuration.hunt.simulate = args.simulate
        self.configuration.hunt.target_rooms = []
        if args.rooms and len(args.rooms) > 0:
            for sublist in args.rooms:
                if isinstance(sublist, list):
                    self.configuration.hunt.target_rooms += sublist
                else:
                    self.configuration.hunt.target_rooms.append(sublist)
