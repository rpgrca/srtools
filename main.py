"""Main module."""
import sys
from srtools.manager.showroommanager import ShowroomManager
from srtools.manager.servicesmanager import ServicesManager
from srtools.utils.commandlineparser import CommandLineParser


def main(args):
    """Main function."""
    parser = CommandLineParser()
    configuration = parser.parse(args)
    showroom_manager = ShowroomManager(configuration)
    services_manager = ServicesManager(configuration, showroom_manager)

    action = services_manager.actions_factory.create(configuration.chosen,
                                                     configuration,
                                                     services_manager)
    action.execute()


if __name__ == "__main__":
    main(sys.argv[1:])
