"""Profile configuration parser."""
from srtools.configuration.configuration import SelectedConfiguration
from srtools.utils.commandline.connection import Connection

class Profile(Connection):
    """Profile parser."""
    def __init__(self, configuration, parser):
        """Constructor for the Profile option."""
        super(Profile, self).__init__(configuration, parser)

    def setup(self, subparsers):
        """Setups the parser for the Profile option."""
        parent = super(Profile, self).setup(subparsers)
        parser = subparsers.add_parser('profile', parents=[parent])
        parser.add_argument('-n', '--name', help="selected username", required=True)
        parser.add_argument('-tl', '--trim_left', default="")
        parser.add_argument('-tt', '--trim_top', default="")
        parser.add_argument('-tr', '--trim_right', default="")
        parser.add_argument('-tb', '--trim_bottom', default="")
        parser.add_argument('-tw', '--trim_width', default="")
        parser.add_argument('-th', '--trim_height', default="")
        parser.add_argument('-tow', '--trim_origin_width', default="")
        parser.add_argument('-toh', '--trim_origin_height', default="")
        parser.add_argument('-p', '--profile_image', default="")
        parser.add_argument('-a', '--avatar_id', default="", type=self._convert_avatar)
        parser.add_argument('-d', '--description', default="")
        parser.set_defaults(func=self.parse)
        return parser

    def parse(self, args):
        """Modifies user profile."""
        super(Profile, self).parse(args)
        if self.configuration.chosen == SelectedConfiguration.UNDEFINED:
            self.configuration.chosen = SelectedConfiguration.PROFILE
            self.configuration.profile.name = args.name
            self.configuration.profile.trim_left = args.trim_left
            self.configuration.profile.trim_top = args.trim_top
            self.configuration.profile.trim_right = args.trim_right
            self.configuration.profile.trim_bottom = args.trim_bottom
            self.configuration.profile.trim_width = args.trim_width
            self.configuration.profile.trim_height = args.trim_height
            self.configuration.profile.trim_origin_width = args.trim_origin_width
            self.configuration.profile.trim_origin_height = args.trim_origin_height
            self.configuration.profile.profile_image = args.profile_image
            self.configuration.profile.avatar_id = args.avatar_id
            self.configuration.profile.description = args.description
