"""Command line parser factory."""
from srtools.utils.loggingutils import log_error
from srtools.utils.commandline.gather import Gather
from srtools.utils.commandline.count import Count
from srtools.utils.commandline.throw import Throw
from srtools.utils.commandline.list import List
from srtools.utils.commandline.track import Track
from srtools.utils.commandline.online import Online
from srtools.utils.commandline.lottery import Lottery
from srtools.utils.commandline.connection import Connection
from srtools.utils.commandline.watch import Watch
from srtools.utils.commandline.test import Test
from srtools.utils.commandline.profile import Profile
from srtools.utils.commandline.daemon import Daemon
from srtools.utils.commandline.capture import Capture
from srtools.utils.commandline.message import Message
from srtools.utils.commandline.hunt import Hunt
from srtools.utils.commandline.stalk import Stalk

class CommandLineParserFactory(object):
    """Command line parser factory"""

    @staticmethod
    def create(args, configuration, parser):
        """Returns the requested parser."""
        option = args.upper()
        result = None

        if option == "CAPTURE":
            result = Capture(configuration, parser)
        elif option == "CONNECTION":
            result = Connection(configuration, parser)
        elif option == "COUNT":
            result = Count(configuration, parser)
        elif option == "DAEMON":
            result = Daemon(configuration, parser)
        elif option == "GATHER":
            result = Gather(configuration, parser)
        elif option == "LIST":
            result = List(configuration, parser)
        elif option == "LOTTERY":
            result = Lottery(configuration, parser)
        elif option == "ONLINE":
            result = Online(configuration, parser)
        elif option == "PROFILE":
            result = Profile(configuration, parser)
        elif option == "TEST":
            result = Test(configuration, parser)
        elif option == "THROW":
            result = Throw(configuration, parser)
        elif option == "TRACK":
            result = Track(configuration, parser)
        elif option == "WATCH":
            result = Watch(configuration, parser)
        elif option == "MESSAGE":
            result = Message(configuration, parser)
        elif option == "HUNT":
            result = Hunt(configuration, parser)
        elif option == "STALK":
            result = Stalk(configuration, parser)
        else:
            log_error(f"Unkonwn action ({option})")

        return result
