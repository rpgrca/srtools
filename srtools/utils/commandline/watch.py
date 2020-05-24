"""Watch configuration parser."""
from srtools.configuration.configuration import SelectedConfiguration
from srtools.utils.commandline.base import IConfigurationInterface

class Watch(IConfigurationInterface):
    """Watch parser."""
    def __init__(self, configuration, parser):
        """Constructor for the Watch option."""
        super(Watch, self).__init__(configuration, parser)

    def setup(self, subparsers):
        """Setups the parser for the Watch option."""
        parser = subparsers.add_parser('watch')
        parser.add_argument('-r', '--rooms', help='list of rooms to track', nargs="+",
                            type=self._convert_group, default={}, required=True)
        parser.add_argument('-s', '--skip-count', help='do not count in room (default: %s)' %
                            self.configuration.watch.skip_count, action='store_true')
        parser.add_argument('-n', '--skip-throw', help='do not throw items (default: %s)' %
                            self.configuration.watch.skip_throw, action='store_true')
        parser.add_argument('-d', '--delay', type=int, default=self.configuration.watch.delay,
                            help='delay between messages (default: %s)' %
                            self.configuration.watch.delay)
        parser.add_argument('-c', '--capture', help='capture information (default: %s)' %
                            self.configuration.watch.capture, action='store_true',
                            default=self.configuration.watch.capture)
        parser.set_defaults(func=self.parse)
        return parser

    def parse(self, args):
        """Watch a room."""
        if self.configuration.chosen == SelectedConfiguration.UNDEFINED:
            self.configuration.chosen = SelectedConfiguration.WATCH
            self.configuration.watch.delay = args.delay
            self.configuration.watch.skip_count = args.skip_count
            self.configuration.watch.skip_throw = args.skip_throw
            self.configuration.watch.capture = args.capture

            if args.rooms is not None and len(args.rooms) > 0:
                self.configuration.watch.target_rooms = [j for i in args.rooms for j in i] \
                                                        if len(args.rooms) > 1 else args.rooms[0]
