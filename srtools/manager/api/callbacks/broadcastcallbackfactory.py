"""Broadcast callback factory"""
from srtools.manager.api.callbacks.defaultbroadcastcallback import DefaultBroadcastCallback
from srtools.manager.api.callbacks.coloredbroadcastcallback import ColoredBroadcastCallback
from srtools.manager.api.callbacks.watchbroadcastcallback import WatchBroadcastCallback
from srtools.manager.api.callbacks.trackbroadcastcallback import TrackBroadcastCallback
from srtools.manager.api.callbacks.readablebroadcastcallback import ReadableBroadcastCallback

class BroadcastCallbackFactory(object):
    """Broadcast callback factory"""
    def __init__(self):
        self._callbacks = {
            WatchBroadcastCallback(None, None).alias(): WatchBroadcastCallback,
            ColoredBroadcastCallback(None, None).alias(): ColoredBroadcastCallback,
            DefaultBroadcastCallback(None, None).alias(): DefaultBroadcastCallback,
            TrackBroadcastCallback(None, None).alias(): TrackBroadcastCallback,
            ReadableBroadcastCallback(None, None).alias(): ReadableBroadcastCallback
        }

    def create(self, handler, configuration, room):
        """
        Create callback handler by alias.
        :param handler: alias of handler
        :type handler: string
        :param configuration: current configuration
        :type configuration: Configuration
        :param room: The room to track.
        :type room: Room
        :returns: A callback handler.
        :rtype: DefaultBroadcastCallback
        """
        if handler in self._callbacks:
            return self._callbacks[handler](configuration, room)

    @property
    def available_handlers(self):
        """
        List of available callback handlers.
        :returns: List of callbacks.
        :rtype: string{}
        """
        return self._callbacks.keys()
