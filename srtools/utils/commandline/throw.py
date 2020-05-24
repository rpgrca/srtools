"""Throw configuration parser."""
from srtools.configuration.configuration import SelectedConfiguration
from srtools.utils.commandline.connection import Connection

class Throw(Connection):
    """Throw parser."""
    def __init__(self, configuration, parser):
        """Constructor for the Count option."""
        super(Throw, self).__init__(configuration, parser)

    def setup(self, subparsers):
        """Setups the parser for the throw option."""
        parent = super(Throw, self).setup(subparsers)
        parser = subparsers.add_parser('throw', parents=[parent])
        parser.add_argument('target_room', help='target room id or shortcut',
                            type=self._convert_room)
        parser.add_argument('-e', '--everything', help='throw everything (default: %s)' %
                            self.configuration.throw.everything, action='store_true',
                            default=self.configuration.throw.everything)
        parser.add_argument('-s', '--step', default=self.configuration.throw.step, type=int,
                            help='number of items to throw at the same time (default: %s)' %
                            self.configuration.throw.step)
        parser.add_argument('-t', '--threads', default=self.configuration.throw.threads,
                            help='number of threads to use (default: %s)' %
                            self.configuration.throw.threads, type=int)
        parser.add_argument('-i', '--items', help='list of items to throw', nargs="+",
                            type=self._parse_items, default={})
        parser.add_argument('-f', '--force', help='force throwing normal items (default: %s)' %
                            self.configuration.throw.force, action='store_true')
        parser.add_argument('-o', '--ordered', help='throw items in order (default: %s)' %
                            self.configuration.throw.ordered, action='store_true')
        parser.add_argument('--steal-avatar', help='steals avatar from broadcast (default: %s)' %
                            self.configuration.throw.steal_avatar, action='store_true')
        parser.set_defaults(func=self.parse)
        return parser

    def parse(self, args):
        """Throw items."""
        super(Throw, self).parse(args)
        if self.configuration.chosen == SelectedConfiguration.UNDEFINED:
            self.configuration.chosen = SelectedConfiguration.THROW
            self.configuration.throw.target_room = args.target_room
            self.configuration.throw.everything = args.everything
            self.configuration.throw.threads = args.threads
            self.configuration.throw.step = args.step
            self.configuration.throw.force = args.force
            self.configuration.throw.ordered = args.ordered
            self.configuration.throw.steal_avatar = args.steal_avatar
            if args.items is not None and len(args.items) > 0:
                self.configuration.throw.items = [x[0] for x in args.items] \
                                                 if len(args.items) > 1 else args.items[0]
