"""Gather configuration parser."""
from srtools.configuration.configuration import SelectedConfiguration
from srtools.utils.commandline.connection import Connection

class Gather(Connection):
    """Gather parser."""
    def __init__(self, configuration, parser):
        """Constructor for the Gather option."""
        super(Gather, self).__init__(configuration, parser)

    def setup(self, subparsers):
        """Setups the parser for the gather option."""
        parent = super(Gather, self).setup(subparsers)
        parser = subparsers.add_parser('gather', parents=[parent])
        parser.add_argument('-s', '--source', choices=['official', 'amateur'],
                            default='official' if self.configuration.gather.official \
                            else 'amateur',
                            help='gather from official rooms (default: %s)' %
                            'official' if self.configuration.gather.official else 'amateur')
        parser.add_argument('-w', '--use-twitter', help='Use Twitter bonus (default: %s)' %
                            self.configuration.gather.use_twitter, action='store_true',
                            default=self.configuration.gather.use_twitter)
        parser.add_argument('-u', '--use-bonus', help='Use View bonus (default: %s)' %
                            self.configuration.gather.use_bonus, action='store_true',
                            default=self.configuration.gather.use_bonus)
        parser.add_argument('-t', '--threads', default=self.configuration.gather.threads,
                            type=int, help='number of threads to use (default: %s)' %
                            self.configuration.gather.threads)
        parser.add_argument('-o', '--overfill', default=self.configuration.gather.overfill,
                            help='try filling over capacity (default: %s)'
                            % self.configuration.gather.overfill, action='store_true')
        parser.add_argument('-f', '--force', default=self.configuration.gather.force,
                            help='forcing filling (default: %s)' %
                            self.configuration.gather.force, action='store_true')
        parser.set_defaults(func=self.parse)
        return parser

    def parse(self, args):
        """Gather items."""
        super(Gather, self).parse(args)
        if args.use_twitter or args.use_bonus:
            self.configuration.chosen = SelectedConfiguration.GATHER
            self.configuration.gather.use_twitter = args.use_twitter
            self.configuration.gather.use_bonus = args.use_bonus
            self.configuration.gather.official = True if args.source == 'official' else False
            self.configuration.gather.threads = args.threads
            self.configuration.gather.overfill = args.overfill
            self.configuration.gather.force = args.force
        else:
            self.parser.error("At least one of --use-twitter or --use-bonus is required.")
