"""Track configuration parser."""
from srtools.configuration.configuration import SelectedConfiguration
from srtools.utils.commandline.connection import Connection

class Track(Connection):
    """Track parser."""
    def __init__(self, configuration, parser):
        """Constructor for the Track option."""
        super(Track, self).__init__(configuration, parser)

    def setup(self, subparsers):
        """Setups the parser for the Track option."""
        parent = super(Track, self).setup(subparsers)
        parser = subparsers.add_parser('track', parents=[parent])
        # TODO: Agregar soporte para kykz / ngzk, que se pueda acumular grupos
        parser.add_argument('-r', '--rooms', help='list of rooms to track', nargs="+",
                            type=self._convert_group, default={})
        parser.add_argument('-d', '--delay', type=int, default=self.configuration.track.delay,
                            help='delay between track (default: %s seconds)' %
                            self.configuration.track.delay)
        parser.add_argument('-t', '--target-file', help='target log file (default: %s)' %
                            self.configuration.track.target_file,
                            default=self.configuration.track.target_file)
        parser.add_argument('-s', '--save', action='store_true', help='save JSONs (default: %s)' %
                            self.configuration.track.save, default=self.configuration.track.save)
        parser.add_argument('-c', '--capture', help='capture information (default: %s)' %
                            self.configuration.track.capture, action='store_true',
                            default=self.configuration.track.capture)
        parser.set_defaults(func=self.parse)
        return parser

    def parse(self, args):
        """Track items."""
        super(Track, self).parse(args)
        self.configuration.chosen = SelectedConfiguration.TRACK
        self.configuration.track.delay = args.delay
        self.configuration.track.save = args.save
        self.configuration.track.target_file = args.target_file
        self.configuration.track.capture = args.capture
        if args.rooms is not None and len(args.rooms) > 0:
            self.configuration.track.target_rooms = [j for i in args.rooms for j in i] \
                                                    if len(args.rooms) > 1 else args.rooms[0]
