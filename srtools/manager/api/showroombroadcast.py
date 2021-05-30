"""Low level routines for SHOWROOM connection."""
import socket
import threading
import srtools.manager.api.message
from srtools.manager.api.callbacks.defaultbroadcastcallback import DefaultBroadcastCallback
from srtools.utils.errorprint import print_error

class ShowroomBroadcast(object):
    """Handles live communication with SHOWROOM."""
    _RECV_BUFFER_SIZE = 4096
    _PING_TIMEOUT = 60

    # Message format
    _LOWLEVEL_SUBSCRIBE = srtools.manager.api.message.MESSAGE_HEADER_SUB + "\t%s\n"
    _LOWLEVEL_QUIT = srtools.manager.api.message.MESSAGE_HEADER_QUIT + "\n"
    _LOWLEVEL_PING = srtools.manager.api.message.MESSAGE_HEADER_PING + "\tshowroom\n"

    _remaining_data = bytearray()
    _room = None
    _user = None
    _ping_task = None
    _configuration = None
    _connected_socket = None

    def __init__(self, configuration, room, user):
        self._configuration = configuration
        self._room = room
        self._user = user
        self._ping_task = threading.Timer(self._PING_TIMEOUT, self._do_ping)
        self._connected_socket = None

    def _send_message(self, message):
        """
        Send a message to the SHOWROOM server.
        :param message: Message to send.
        :type message: string
        """
        self._connected_socket.sendall(message.encode('utf8'))

    def _connect(self, address, port):
        """
        Connect to SHOWROOM server.
        :param address: Address to connect.
        :type address: string
        :param port: Port where to connect.
        :type port: int
        """
        self._connected_socket = socket.create_connection((address, port))

    def _subscribe(self, key):
        """
        Subscribe to the given room.
        :param key: Key for broadcast.
        :type key: string
        """
        subscription = self._LOWLEVEL_SUBSCRIBE % key
        self._send_message(subscription)

    def _quit(self):
        """End communication with room."""
        self._send_message(self._LOWLEVEL_QUIT)

    def _do_ping(self):
        """Execute a ping, set the new ping."""
        self._ping()
        self._ping_task = threading.Timer(self._PING_TIMEOUT, self._do_ping)
        self._ping_task.start()

    def _ping(self):
        """Send ping (should be sent every 60 seconds)."""
        self._send_message(self._LOWLEVEL_PING)

    def _receive(self):
        """
        Receive information from connection.
        :returns: List of full messages to process.
        :rtype: string[]
        """
        try:
            message_list = []
            received_data = self._connected_socket.recv(self._RECV_BUFFER_SIZE)
            if received_data:
                temp_received = self._remaining_data;
                temp_received.extend(received_data)
                received_data = temp_received
                if received_data.find(b"\n") > -1:
                    index = received_data.rfind(b"\n") + 1
                    result = received_data[:index]

                    self._remaining_data = received_data[index:]

                    #result = result.replace("\xe9", "e")
                    result = result.decode("utf-8", "replace")
                    message_list = filter(None, result.split("\n"))
                else:
                    self._remaining_data = received_data
                    message_list = []

        except Exception as err:
            print_error(err)

        return message_list

    def _receive_old(self):
        """
        Receive information from connection.
        :returns: List of full messages to process.
        :rtype: string[]
        """
        try:
            received_data = self._connected_socket.recv(self._RECV_BUFFER_SIZE)
            if received_data:
                received_data = received_data.decode("utf-8")

            received_data = self._remaining_data + received_data
            if received_data.find("\n") > -1:
                index = received_data.rfind("\n") + 1
                result = received_data[:index]

                self._remaining_data = received_data[index:]
                message_list = filter(None, result.split("\n"))
            else:
                self._remaining_data = received_data
                message_list = []
        except Exception as err:
            print_error(err)

        return message_list

    def do_communication(self, callback=None):
        """
        Execute communication loop
        :param callback: Callback to call for each received message.
        :type callback: function
        """
        continue_processing = True
        if callback is None:
            callback = DefaultBroadcastCallback(self._configuration, self._room)

        self._connect(self._room.live.broadcast_host, self._room.live.broadcast_port)
        self._subscribe(self._room.live.broadcast_key)
        self._ping_task.start()

        callback.initialize()
        while continue_processing:
            message_list = self._receive()

            if message_list:
                for message in message_list:
                    callback.new_message(message)
                    continue_processing = callback.process_message(message)
            else:
                continue_processing = callback.empty_message()


        self._ping_task.cancel()
        self._quit()
        callback.terminate()
