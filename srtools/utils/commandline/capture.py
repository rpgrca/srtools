"""Capture configuration parser."""
import argparse
from srtools.configuration.configuration import SelectedConfiguration
from srtools.utils.commandline.base import IConfigurationInterface
from srtools.manager.api.callbacks.broadcastcallbackfactory import BroadcastCallbackFactory

class CaptureBase(IConfigurationInterface):
    """Capture base parser."""
    def __init__(self, configuration, parser):
        """Constructor for the Capture option."""
        super(CaptureBase, self).__init__(configuration, parser)

    def setup(self, subparsers):
        """Setups the parser for the Capture option."""
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('-o', '--output', help='capture target filename (default: %s)' %
                            self.configuration.capture.output)
        return parser

    def parse(self, args):
        """Test items."""
        self.configuration.capture.output = args.output

class Capture(CaptureBase):
    """Capture parser."""
    def __init__(self, configuration, parser):
        """Constructor for the Capture option."""
        super(Capture, self).__init__(configuration, parser)

    def setup(self, subparsers):
        """Setups the parser for the Capture option."""
        parent = super(Capture, self).setup(subparsers)
        parser = subparsers.add_parser('capture', parents=[parent])
        parser.add_argument('target_room', help='target room id or shortcut',
                            type=self._convert_room)
        parser.add_argument('-t', '--type', default=self.configuration.capture.type,
                            choices=BroadcastCallbackFactory().available_handlers,
                            help='type of handler to use (default: %s)' %
                            self.configuration.capture.type)

        parser.set_defaults(func=self.parse)

    def parse(self, args):
        """Parsed items."""
        super(Capture, self).parse(args)
        self.configuration.chosen = SelectedConfiguration.CAPTURE
        self.configuration.capture.target_room = args.target_room
        self.configuration.capture.type = args.type
