"""List configuration parser."""
from srtools.configuration.configuration import SelectedConfiguration
from srtools.utils.commandline.connection import Connection

class List(Connection):
    """List parser."""
    def __init__(self, configuration, parser):
        """Constructor for the List option."""
        super(List, self).__init__(configuration, parser)

    def setup(self, subparsers):
        """Setups the parser for the list option."""
        parent = super(List, self).setup(subparsers)
        parser = subparsers.add_parser('list', parents=[parent])
        parser.add_argument('target', choices=['avatar', 'user', 'group'], default='avatar',
                            help='what to list')
        parser.set_defaults(func=self.parse)
        return parser

    def parse(self, args):
        """List items."""
        super(List, self).parse(args)
        if args.target == 'avatar':
            self.configuration.chosen = SelectedConfiguration.LIST_AVATARS
        elif args.target == 'user':
            self.configuration.chosen = SelectedConfiguration.LIST_USERS
        elif args.target == 'group':
            self.configuration.chosen = SelectedConfiguration.LIST_GROUPS
