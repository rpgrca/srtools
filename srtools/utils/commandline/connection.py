"""Connection configuration parser."""
import argparse
from srtools.utils.commandline.base import IConfigurationInterface

class Connection(IConfigurationInterface):
    """Connection parser."""
    def __init__(self, configuration, parser):
        """Constructor for the Connection option."""
        IConfigurationInterface.__init__(self, configuration, parser)

    def setup(self, subparsers):
        """Setups the parser for the Connection option."""
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('--timeout', required=False, help='timeout (default: %s)' %
                            self.configuration.connection.timeout, type=int,
                            default=self.configuration.connection.timeout)
        parser.add_argument('--user-agent', required=False, help='custom user agent (default: %s)'%
                            self.configuration.connection.user_agent,
                            default=self.configuration.connection.user_agent)
        parser.add_argument('--cookies', help='Browser from where to pick cookies (default: %s)' %
                            self.configuration.connection.cookies, choices=['firefox', 'chrome'],
                            required=False, default=self.configuration.connection.cookies)
        parser.add_argument('--username', required=False, help='Username to use')
        parser.add_argument('--password', required=False, help='Password to use')
        return parser

    def parse(self, args):
        """Connection routines."""
        self.configuration.connection.timeout = args.timeout
        self.configuration.connection.user_agent = args.user_agent
        self.configuration.connection.cookies = args.cookies
        self.configuration.connection.username = args.username
        self.configuration.connection.password = args.password
