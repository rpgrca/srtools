"""Command line parser."""
import sys
import argparse
import Tkinter
import tkSimpleDialog
from srtools.configuration.configuration import Configuration
from srtools.utils.commandline.factory import CommandLineParserFactory

class CommandLineParser(object):
    """Command line parser."""
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Process SHOWROOM calls.')
        self.configuration = Configuration()
        self.options = [
            CommandLineParserFactory.create("capture", self.configuration, self.parser),
            CommandLineParserFactory.create("count", self.configuration, self.parser),
            CommandLineParserFactory.create("gather", self.configuration, self.parser),
            CommandLineParserFactory.create("list", self.configuration, self.parser),
            CommandLineParserFactory.create("lottery", self.configuration, self.parser),
            CommandLineParserFactory.create("online", self.configuration, self.parser),
            CommandLineParserFactory.create("profile", self.configuration, self.parser),
            CommandLineParserFactory.create("test", self.configuration, self.parser),
            CommandLineParserFactory.create("throw", self.configuration, self.parser),
            CommandLineParserFactory.create("track", self.configuration, self.parser),
            CommandLineParserFactory.create("watch", self.configuration, self.parser),
            CommandLineParserFactory.create("message", self.configuration, self.parser),
            CommandLineParserFactory.create("hunt", self.configuration, self.parser)
        ]

    def parse(self, args):
        """Parse arguments."""
        subparsers = self.parser.add_subparsers()
        for parser in self.options:
            parser.setup(subparsers)

        if not args:
            try:
                root = Tkinter.Tk()
                root.withdraw()
                text = tkSimpleDialog.askstring("Showroom Manager", "Enter command line:")
                if text is not None and text:
                    args = text.split(' ')
            except StandardError as err:
                print err

        args = self.parser.parse_args(args)
        args.func(args)

        return self.configuration

if __name__ == "__main__":
    CommandLineParser().parse(sys.argv[1:])
