"""Count configuration parser."""
from srtools.configuration.configuration import SelectedConfiguration
from srtools.utils.commandline.connection import Connection

class Count(Connection):
    """Count parser."""
    def __init__(self, configuration, parser):
        """Constructor for the Count option."""
        super(Count, self).__init__(configuration, parser)

    def setup(self, subparsers):
        """Setups the parser for the Count option."""
        parent = super(Count, self).setup(subparsers)
        parser = subparsers.add_parser('count', parents=[parent])
        parser.add_argument('target_room', help='target room id or shortcut, 0 for all',
                            type=self._convert_room)
        parser.add_argument('-l', '--minimum-live-id', help='minimum live id (default: %s)' %
                            self.configuration.count.minimum_live_id, type=int,
                            default=self.configuration.count.minimum_live_id)
        parser.add_argument('-t', '--threads', default=self.configuration.count.threads,
                            type=int, help='number of threads to use (default: %s)' %
                            self.configuration.count.threads)
        parser.add_argument('-s', '--start', type=int, help='start value (default: %s)' %
                            self.configuration.count.start, default=self.configuration.count.start)
        parser.add_argument('-e', '--end', type=int, help='end value (default: %s)' %
                            self.configuration.count.end, default=self.configuration.count.end)
        parser.add_argument('-m', '--message', help='custom message after counting to %s' %
                            self.configuration.count.end)
        parser.add_argument('-d', '--delay', type=float, help='message delay (default: %s)' %
                            self.configuration.count.delay, default=self.configuration.count.delay)
        parser.add_argument('-x', '--max-tries', default=self.configuration.count.max_tries,
                            help='max attempts (default: %s)' % self.configuration.count.max_tries)
        parser.add_argument('-v', '--no-visit', default=self.configuration.count.no_visit,
                            help='don\'t mark room as visited (default: %s)' %
                            self.configuration.count.no_visit, action='store_true')
        parser.add_argument('-r', '--repeat', default=self.configuration.count.repeat, type=int,
                            help='repeat (default: %s)' % self.configuration.count.repeat)
        parser.add_argument('-k', '--skip', default=self.configuration.count.skip,
                            help='rooms to skip', action='append', type=self._convert_room)
        parser.set_defaults(func=self.parse)
        return parser

    def parse(self, args):
        """Fills up the configuration with the parser results."""
        super(Count, self).parse(args)
        if self.configuration.chosen == SelectedConfiguration.UNDEFINED:
            self.configuration.chosen = SelectedConfiguration.COUNT
            self.configuration.count.target_room = args.target_room
            self.configuration.count.threads = args.threads
            self.configuration.count.message = args.message
            self.configuration.count.minimum_live_id = args.minimum_live_id
            self.configuration.count.start = args.start
            self.configuration.count.end = args.end
            self.configuration.count.delay = args.delay
            self.configuration.count.max_tries = args.max_tries
            self.configuration.count.no_visit = args.no_visit
            self.configuration.count.repeat = args.repeat
            self.configuration.count.skip = args.skip
            self.configuration.login.username = args.username
            self.configuration.login.password = args.password
