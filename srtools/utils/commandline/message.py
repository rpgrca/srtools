"""Message configuration parser."""
from srtools.configuration.configuration import SelectedConfiguration
from srtools.utils.commandline.connection import Connection

class Message(Connection):
    """Message parser."""
    def __init__(self, configuration, parser):
        """Constructor for the Message option."""
        super(Message, self).__init__(configuration, parser)

    def setup(self, subparsers):
        """Setups the parser for the Message option."""
        parent = super(Message, self).setup(subparsers)
        parser = subparsers.add_parser('message', parents=[parent])
        parser.add_argument('target_room', help='target room id', type=self._convert_room)
        parser.add_argument('-m', '--message', help='message to send')
        parser.add_argument('-x', '--max-tries', default=self.configuration.count.max_tries,
                            help='max attempts (default: %s)' % self.configuration.count.max_tries)
        parser.add_argument('-v', '--no-visit', default=self.configuration.count.no_visit,
                            help='don\'t mark room as visited (default: %s)' %
                            self.configuration.count.no_visit, action='store_true')
        parser.set_defaults(func=self.parse)
        return parser

    def parse(self, args):
        """Fills up the configuration with the parser results."""
        super(Message, self).parse(args)
        if self.configuration.chosen == SelectedConfiguration.UNDEFINED:
            self.configuration.chosen = SelectedConfiguration.MESSAGE
            self.configuration.message.target_room = args.target_room
            self.configuration.message.message = args.message
            self.configuration.message.max_tries = args.max_tries
            #self.configuration.count.no_visit = args.no_visit
            self.configuration.login.username = args.username
            self.configuration.login.password = args.password
