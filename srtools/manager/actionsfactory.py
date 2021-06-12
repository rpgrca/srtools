"""Actions Factory."""
import textwrap
from abc import ABCMeta, abstractmethod

from srtools.configuration.configuration import SelectedConfiguration
from srtools.utils.loggingutils import log_trace, log_error
from srtools.manager.showroommanager import RoomsManager
from srtools.manager.api.callbacks.broadcastcallbackfactory import BroadcastCallbackFactory

class ActionsFactory(object):
    """Actions factory."""
    class BaseAction(object):
        """Base class for all actions handled by the program."""
        __metaclass__ = ABCMeta

        configuration = None
        services_manager = None

        def __init__(self, configuration, services_manager):
            """
            :param configuration: The current configuration.
            :type configuration: Configuration
            :param services_manager: The current services manager.
            :type services_manager: ServicesManager
            """
            self.configuration = configuration
            self.services_manager = services_manager

        @abstractmethod
        def execute(self):
            """
            Abstract method, executes the given action.
            :returns: True if the action was executed correctly, False otherwise.
            :rtype: bool
            """
            pass

    class CaptureAction(BaseAction):
        """Handler for Capture action."""
        def __init__(self, configuration, services_manager):
            super(ActionsFactory.CaptureAction, self).__init__(configuration, services_manager)

        def execute(self):
            # TODO: Si no se da un nombre de archivo, que lo cree solo como watch
            room = self.services_manager.find_room(self.configuration.capture.target_room)
            callback = BroadcastCallbackFactory().create(self.configuration.capture.type, self.configuration, room)
            if room:
                self.services_manager.showroom_api.get_live_data(room, self.services_manager.showroom_manager.lives_manager)
                self.services_manager.do_communication(room, callback)
            else:
                print("Room offline.")

    class MessageAction(BaseAction):
        """Handler for Message action."""
        def __init__(self, configuration, services_manager):
            super(ActionsFactory.MessageAction, self).__init__(configuration, services_manager)

        def execute(self):
            room = self.services_manager.find_room(self.configuration.message.target_room)
            if room:
                self.services_manager.showroom_api.send_comment(room.live, \
                    self.configuration.message.message)

    class CountAction(BaseAction):
        """Handler for Count action."""
        def __init__(self, configuration, services_manager):
            super(ActionsFactory.CountAction, self).__init__(configuration, services_manager)

        def execute(self):
            log_trace("Executing Count action")
            rooms_filter = self.services_manager.showroom_manager.rooms_manager.create_filter()
            rooms_filter.order_by = RoomsManager.RoomsSort.LIVE_ID_ASC
            rooms_filter.room_id = self.configuration.count.target_room
            rooms = self.services_manager.showroom_manager.rooms_manager.rooms(rooms_filter)
            rooms = [x for x in rooms if x.room_id not in self.configuration.count.skip]
            if self.configuration.count.minimum_live_id > 0:
                rooms = [x for x in rooms \
                         if x.live.live_id > self.configuration.count.minimum_live_id]

            if self.services_manager.do_count_in_rooms(rooms):
                print(f"Maximum value: {rooms[-1].live.live_id}")

    class ThrowAction(BaseAction):
        """Handler for Throw action."""
        def __init__(self, configuration, services_manager):
            super(ActionsFactory.ThrowAction, self).__init__(configuration, services_manager)

        def execute(self):
            room = self.services_manager.find_room(self.configuration.throw.target_room)
            if room is not None:
                self.services_manager.do_throw_normal_items(room, self.configuration.throw.items)
            else:
                print("Room offline.")

    class WatchAction(BaseAction):
        """Handler for Watch action."""
        def __init__(self, configuration, services_manager):
            super(ActionsFactory.WatchAction, self).__init__(configuration, services_manager)

        def execute(self):
            if len(self.configuration.watch.target_rooms) > 1:
                self.services_manager.do_watch_rooms(self.configuration.watch.target_rooms,
                                                     self.configuration.watch.delay)
            else:
                self.services_manager.do_watch_room(self.configuration.watch.target_rooms[0],
                                                    self.configuration.watch.delay)

    class GatherAction(BaseAction):
        """Handler for Gather action."""
        def __init__(self, configuration, services_manager):
            super(ActionsFactory.GatherAction, self).__init__(configuration, services_manager)

        def execute(self):
            rooms_filter = self.services_manager.showroom_manager.rooms_manager.create_filter()
            rooms_filter.official = self.configuration.gather.official
            rooms = self.services_manager.showroom_manager.rooms_manager.rooms(rooms_filter)
            self.services_manager.do_reload_items(rooms)

    class TrackAction(BaseAction):
        """Handler for Track action."""
        def __init__(self, configuration, services_manager):
            super(ActionsFactory.TrackAction, self).__init__(configuration, services_manager)

        def execute(self):
            self.services_manager.do_track(self.configuration.track.target_file,
                                           self.configuration.track.target_rooms)

    class HuntAction(BaseAction):
        """Handler for Hunt action."""
        def __init__(self, configuration, services_manager):
            super(ActionsFactory.HuntAction, self).__init__(configuration, services_manager)

        def execute(self):
            self.services_manager.do_hunt_avatars(self.configuration.hunt.target_rooms)

    class ProfileAction(BaseAction):
        """Handler for Profile action."""
        def __init__(self, configuration, services_manager):
            super(ActionsFactory.ProfileAction, self).__init__(configuration, services_manager)

        def execute(self):
            self.services_manager.showroom_manager.showroom_api.update_profile(self.configuration.profile)

    class LotteryAction(BaseAction):
        """Handler for Lottery action."""
        def __init__(self, configuration, services_manager):
            super(ActionsFactory.LotteryAction, self).__init__(configuration, services_manager)

        def execute(self):
            avatar = None
            while avatar is None or int(avatar.get('grade')) != self.configuration.lottery.target:
                avatar = self.services_manager.showroom_manager.showroom_api.execute_lottery( \
                             self.configuration.lottery.name)
                print(avatar)

    class OnlineAction(BaseAction):
        """Handler for Online action."""
        def __init__(self, configuration, services_manager):
            super(ActionsFactory.OnlineAction, self).__init__(configuration, services_manager)

        def execute(self):
            result = self.services_manager.showroom_manager.showroom_api.is_online( \
                         self.configuration.online.target_room)
            print(f"Room {self.configuration.online.target_room} is {'online' if result else 'not online'}")
                                     
            return result

    class TestAction(BaseAction):
        """Handler for Test action."""
        def __init__(self, configuration, services_manager):
            super(ActionsFactory.TestAction, self).__init__(configuration, services_manager)

        def execute(self):
            room = self.services_manager.showroom_manager.rooms_manager.find(self.configuration.test.target_room)
            if room is not None:
                pass

    class ListBaseAction(BaseAction):
        """Base handler for List action."""
        def __init__(self, configuration, services_manager, keys):
            super(ActionsFactory.ListBaseAction, self).__init__(configuration, services_manager)
            self.keys = sorted(keys)

        def execute(self):
            text = 'Possible values: %s' % (', '.join(self.keys))
            print('\n'.join(textwrap.wrap(text, 80)))

    class ListAvatarAction(ListBaseAction):
        """Handler for ListAvatar action."""
        def __init__(self, configuration, services_manager):
            super(ActionsFactory.ListAvatarAction, self).__init__(
                configuration, services_manager, configuration.favorite_avatars
            )

    class ListUserAction(ListBaseAction):
        """Handler for ListUser action."""
        def __init__(self, configuration, services_manager):
            super(ActionsFactory.ListUserAction, self).__init__(
                configuration, services_manager, configuration.favorite_users
            )

    class ListGroupAction(ListBaseAction):
        """Handler for ListGroup action."""
        def __init__(self, configuration, services_manager):
            super(ActionsFactory.ListGroupAction, self).__init__(
                configuration, services_manager, configuration.favorite_groups
            )

    class StalkAction(BaseAction):
        """Handler for Stalk action."""
        def __init__(self, configuration, services_manager):
            super(ActionsFactory.StalkAction, self).__init__(configuration, services_manager)

        def execute(self):
            self.services_manager.do_stalk_avatars(self.configuration.obtained_avatars.avatars)

    def __init__(self):
        pass

    def create(self, action_id, configuration, services_manager):
        """
        Create an action to execute.
        :param action_id: Action to create.
        :type action_id: SelectedConfiguration
        :param configuration: Configuration to use.
        :type configuration: Configuration
        :param services_manager: Services manager to use.
        :type services_manager: ServicesManager
        :returns: The action to execute, or None if invalid.
        :rtype: BaseAction
        """
        action = None

        if action_id == SelectedConfiguration.COUNT:
            action = self.CountAction(configuration, services_manager)
        elif action_id == SelectedConfiguration.THROW:
            action = self.ThrowAction(configuration, services_manager)
        elif action_id == SelectedConfiguration.WATCH:
            action = self.WatchAction(configuration, services_manager)
        elif action_id == SelectedConfiguration.GATHER:
            action = self.GatherAction(configuration, services_manager)
        elif action_id == SelectedConfiguration.PROFILE:
            action = self.ProfileAction(configuration, services_manager)
        elif action_id == SelectedConfiguration.LOTTERY:
            action = self.LotteryAction(configuration, services_manager)
        elif action_id == SelectedConfiguration.ONLINE:
            action = self.OnlineAction(configuration, services_manager)
        elif action_id == SelectedConfiguration.TRACK:
            action = self.TrackAction(configuration, services_manager)
        elif action_id == SelectedConfiguration.TEST:
            action = self.TestAction(configuration, services_manager)
        elif action_id == SelectedConfiguration.LIST_AVATARS:
            action = self.ListAvatarAction(configuration, services_manager)
        elif action_id == SelectedConfiguration.LIST_USERS:
            action = self.ListUserAction(configuration, services_manager)
        elif action_id == SelectedConfiguration.LIST_GROUPS:
            action = self.ListGroupAction(configuration, services_manager)
        elif action_id == SelectedConfiguration.CAPTURE:
            action = self.CaptureAction(configuration, services_manager)
        elif action_id == SelectedConfiguration.MESSAGE:
            action = self.MessageAction(configuration, services_manager)
        elif action_id == SelectedConfiguration.HUNT:
            action = self.HuntAction(configuration, services_manager)
        elif action_id == SelectedConfiguration.STALK:
            action = self.StalkAction(configuration, services_manager)
        else:
            log_error("Unkonwn action (%s)" % action_id)

        return action
