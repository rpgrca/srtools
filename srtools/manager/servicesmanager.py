"""Services Manager"""
import csv
import os
import random
import time
import json
from datetime import datetime

from pytz import timezone

from srtools.configuration.configuration import BallotGifts, FreeGifts, PaidGifts
from srtools.manager.actionsfactory import ActionsFactory
from srtools.manager.api.callbacks.coloredbroadcastcallback import ColoredBroadcastCallback
from srtools.manager.api.callbacks.watchbroadcastcallback import WatchBroadcastCallback
from srtools.manager.api.callbacks.readablebroadcastcallback import ReadableBroadcastCallback
from srtools.manager.api.showroombroadcast import ShowroomBroadcast
from srtools.manager.basemanager import BaseManager
from srtools.utils.activesleep import activesleep
from srtools.utils.dateformat import formatted_date
from srtools.utils.jsonutils import save_json
from srtools.utils.loggingutils import log_error, log_trace
from srtools.utils.parallel import Parallel


class ServicesManager(BaseManager):
    """Services Manager."""
    _KAHOTARU_ROOM_ID = 97203

    def __init__(self, configuration, showroom_manager):
        super(ServicesManager, self).__init__(configuration, showroom_manager.showroom_api)
        self.actions_factory = ActionsFactory()
        self.showroom_manager = showroom_manager

    def _count_in_room(self, room):
        """
        Executes counting from 1 to 50 in given room.
        :param room: Room where to count.
        :type room: Room
        :returns: True if finished counting, False if failed.
        :rtype: bool
        """
        #log_trace("Counting", extra={"room_id":room.room_id})
        if room is not None and room.live is not None:
            result = True

            if self.configuration.count.start < self.configuration.count.end:
                start = self.configuration.count.start
                end = self.configuration.count.end + 1
                step = 1
            else:
                start = self.configuration.count.end
                end = self.configuration.count.start - 1
                step = -1

            if not self.configuration.count.no_visit:
                self._force_visit(room)

            #for index in range(self.configuration.count.start, self.configuration.count.end + 1):
            cycle = 0
            while cycle < self.configuration.count.repeat:
                cycle += 1

                for index in range(start, end, step):
                    if self.showroom_api.send_comment(room.live, str(index),
                                                      self.configuration.count.max_tries,
                                                      self.configuration.count.delay):
                        print(f"Counting [room: {room.room_id}, name: {room.room_url_key}, live: {room.live.live_id}, {start}-{end}]: {str(index)}")

                        time.sleep(self.configuration.count.delay)
                    else:
                        result = False
                        break

            if self.configuration.count.message is not None:
                self.showroom_api.send_comment(room.live, self.configuration.count.message)
        else:
            result = False

        return result

    def _count_in_rooms(self, rooms):
        """
        Auxiliar method to count in rooms.
        :param rooms: List of rooms to process.
        :type rooms: Room[]
        """
        parallel = Parallel(len(rooms))

        for room in rooms:
            parallel.add_task(rooms.index(room), self._count_in_room, room)

        print(parallel.get_results())

    def _force_visit(self, room):
        """
        Force visiting a room.
        :param room: Room to visit.
        :type room: Room
        :returns: True if visited, False if failed.
        :rtype: bool
        """
        index = 0
        tries = 3

        while index < tries:
            current_user = self.showroom_api.get_current_user(room)
            if current_user is None:
                index = index + 1
            else:
                index = tries

        return current_user is not None

    def _split_array(self, array):
        """
        Split an array in chunks of thread size.
        :param array: Array of items to throw.
        :returns: Array of arrays of items to throw.
        """
        result = []
        index = 0

        while index < len(array):
            result.append(array[index:index + self.configuration.throw.threads])
            index += self.configuration.throw.threads

        return result

    def _throw_gift(self, gift_id, live, num):
        """
        Throw the given amount of gifts in the given broadcast.
        :param gift_id: Gift id to throw.
        :type gift_id: int
        :param live: Live to where throw it.
        :type live: Live
        :param num: Amount of items to throw.
        :type num: int
        :returns: Whether it could throw the gift or not.
        :rtype: string
        """
        items = [e.value for e in PaidGifts]

        if gift_id in items:
            result = self.showroom_api.throw_paid_gift(live, gift_id, num)
        else:
            result = "Invalid paid gift id."

        return result

    def _throw_item(self, gift_id, live, num):
        """
        Throw the given number of items in the given broadcast.
        :param gift_id: Gift id to throw.
        :type gift_id: int
        :param live: Live to where throw it.
        :type live: Live
        :param num: Amount of items to throw.
        :type num: int
        :returns: Whether it could throw the gift or not.
        :rtype: string
        """
        log_trace("Throwing items", extra={"live":live, "gift_id":gift_id, "num":num})
        items = [e.value for e in FreeGifts] + [e.value for e in BallotGifts]

        if gift_id in items:
            result = self.showroom_api.throw_free_gift(live, gift_id, num)
        else:
            result = "None"

        return result

    def _do_hunt_avatar(self, room):
        """
        Prepare and throw items in room to get avatar.
        :param room: Room where to throw.
        :type room: Room
        :returns: Json
        :rtype: json
        """
        free_items = [e.value for e in FreeGifts]
        self.configuration.throw.steal_avatar = True
        self.configuration.throw.everything = True
        items = sorted(self.get_throwable_items(room), key=lambda k: k['free_num'], reverse=True)
        chosen = False
        for item in items:
            if item['gift_id'] in free_items:
                item['free_num'] = 0 if chosen else 1
                chosen = True

        if chosen:
            items = [x for x in items if x['free_num'] > 0 and x['gift_id'] in free_items]
            #self.do_throw_normal_items(room, items)
            return self._throw_item(items[0]['gift_id'], room.live, items[0]['free_num'])
        else:
            return json.loads("{u'error_user_msg': u'Special gifts only while voting is open.', u'message': u'BAD REQUEST', u'code': 1001}")

    def _track_rooms_load_previous_day(self, filename):
        """
        Auxiliar function, load information from previous day.
        Currently unused.
        """
        _ = timezone('Asia/Tokyo')
        last = {}
        with open(filename, "r") as input_file:
            reader = csv.reader(input_file, delimiter='\t')
            for room_id, _, date, _, followers, viewers, points, diff in reader:
                if room_id not in last:
                    last[room_id] = {
                        "points": points, "date": date, "viewers": viewers,
                        "followers": followers, "diff": diff
                    }

    def _do_watch_refresh_manager(self, room_id):
        """
        Refresh Showroom manager and find current room.
        :param room_id: Room id to search.
        :type room_id: int
        :returns: Room for given room_id
        :rtype: Room
        """
        tries = 3
        room = None
        while tries > 0 and room is None:
            print("Trying to refresh manager...")
            tries -= 1
            self.showroom_manager.initialize()
            room = self.showroom_manager.rooms_manager.find(room_id)
            if room is not None:
                live = self.showroom_manager.showroom_api.get_live_data(room, \
                       self.showroom_manager.lives_manager)
                room.live = live

        return room

    def _do_watch_wait(self, room_id, delay):
        """
        Wait until asked room goes online.
        :param room_id: Room id to check.
        :type room_id: int
        :param delay: Seconds to wait between tries.
        :type delay: float
        """
        # TODO: Fix
        # Room 97203 is not online, retrying in 10 seconds.
        # Next broadcast: 2017-06-12 10:30:00 (in -1 day, 23:59:59.833071)
        while not self.showroom_api.is_online(room_id):
            message = "Room %s is not online, retrying in %s seconds." % (room_id, delay)
            next_br = self.showroom_api.get_next_live(room_id)
            if next_br is not None:
                print(f"{message}\n    Next broadcast: {next_br} (in {(next_br - datetime.now())})")
            else:
                print(message)

            time.sleep(delay)

    def _do_watch_check_renewal(self, left, total, extra):
        """
        Callback.
        :param left: Seconds left in timer.
        :type left: int
        :param total: Total amount of seconds waiting.
        :type total: int
        :param extra: Dictionary of extra arguments.
        :type extra: Dictionary
        :returns: True if execution continues, False if stops.
        :rtype: bool
        """
        room = extra["room"]
        result = left

        if room is not None:
            current_date = datetime.now()

            live = self.showroom_manager.showroom_api.get_live_data(room, \
                   self.showroom_manager.lives_manager)

            if live is not None and (room.live is None or room.live.live_id != live.live_id):
                print(f"New live before countdown ended ({left}/{total})! Aborting wait!")
                room.live = live

                self._do_watch_capture(room)
                result = 0
            else:
                result -= (datetime.now() - current_date).seconds

        return result

    def _do_watch_get_capture_filename(self, room):
        """
        Get a filename to capture information from given room.
        :param room: Room to capture.
        :type room: Room
        :returns: The filename to use.
        :rtype: string
        """
        return "watch-%s-%s-%s.txt" % (formatted_date(), str(room.room_url_key),
                                       str(room.live.live_id))

    def _do_track_get_filename(self, date, room):
        """
        Get a filename to capture live information from given room.
        :param date: Date to use.
        :type date: datetime
        :param room: Room to track.
        :type room: Room
        :returns: The filename to use.
        :rtype: string
        """
        return "track-%s-%s-%s-%s.json" % (formatted_date(date), str(room.room_id),
                                           str(room.room_url_key), str(room.live.live_id))

    def _do_track_process_data(self, room, live, date, last):
        """
        :param room: The room to process.
        :type room: Room
        :param live: The calculated live object.
        :type live: Live
        :param date: The date to use.
        :type date: datetime
        :param last: Cache information.
        :type last: string[]
        :returns: The line to add.
        :rtype: string
        """
        line_to_add = ""
        if room.room_id not in last:
            last[room.room_id] = {"points": 0, "viewers": 0, "followers": 0}

        if live.room is not None:
            if last[room.room_id]["points"] != live.room['popularity_point'] or \
               last[room.room_id]["followers"] != live.room['follower_num'] or \
               last[room.room_id]['viewers'] != live.live_res['view_uu']:
                line_to_add = {"id": room.room_id,
                               "key": room.room_url_key,
                               "date": date,
                               "actual_date": datetime.now(),
                               "followers": live.room["follower_num"],
                               "viewers": live.live_res["view_uu"],
                               "points": live.room["popularity_point"],
                               "diff": int(live.room['popularity_point']) - \
                                       int(last[room.room_id]["points"]) \
                                       if int(last[room.room_id]["points"]) != 0 else 0
                              }

            print(f"Updating {room.room_url_key} [R: {room.room_id}, L: {room.live.live_id}, F: {live.room['follower_num']} {(int(live.room['follower_num']) - int(last[room.room_id]['followers']) if int(last[room.room_id]['followers']) != 0 else 0)}, P: {int(line_to_add['points'])} ({int(line_to_add['diff'])})]")

            last[room.room_id]["points"] = live.room['popularity_point']
            last[room.room_id]["followers"] = live.room['follower_num']
            last[room.room_id]["viewers"] = live.live_res['view_uu']

        return line_to_add

    def _do_track_find_official_users(self, live):
        """
        Find official user in given top 10 live.
        :param live: Live to search in.
        :type live: Live
        :returns: Array of names of found users.
        :rtype: string[]
        """
        # TODO: Return tuple "id, rank"
        if live.ranking is not None:
            return list(set(int(x["user_id"]) for x in live.ranking["live_ranking"]) & \
                        self.configuration.favorite_official_users.favorites_set)
        else:
            return None

    def _do_watch_capture(self, room, callback=None):
        """
        Fork a process to capture the messaging.
        :param room: Room to capture.
        :type room: Room
        """
        if self.configuration.watch.capture:
            pid = os.fork()
            if pid > 0:
                print(f"Spawned daemon process {pid}.")
            else:
                pid = os.fork()
                if pid > 0:
                    print(f"Spawned process {pid} to capture communication.")
                    exit(0)
                    os._exit(0)
                else:
                    self.configuration.capture.output = self._do_watch_get_capture_filename(room)
                    if callback is None:
                        callback = WatchBroadcastCallback(self.configuration, room)

                    self.do_communication(room, callback)
                    print(f"Spawned process ended at {datetime.now()}.")
                    os._exit(0)

    """
    ---
    """
    def do_count_in_rooms(self, rooms):
        """
        Count in every room in the given list.
        :param rooms: List of rooms to process.
        :type rooms: Room[]
        """
        result = False
        index = 0
        total = 0
        if rooms:
            rooms_to_process = []

            total = len(rooms)
            for room in rooms:
                index += 1
                if self.showroom_api.is_online(room.room_id):
                    rooms_to_process.append(room)
                    print(f"Processing room {room.room_id} ({index}/{total})")
                else:
                    print(f"Skipping room {room.room_id}, offline." % room.room_id)

                if len(rooms_to_process) >= self.configuration.count.threads:
                    self._count_in_rooms(rooms_to_process)
                    rooms_to_process = []

                time.sleep(5)

            if rooms_to_process:
                self._count_in_rooms(rooms_to_process)

            result = True
        else:
            print("No room to count.")

        return result

    def do_login(self, username, password):
        """Login."""
        self.showroom_api.login(username, password)

    def do_reload_items(self, rooms):
        """Fills items with maximum possible values."""
        index = 0
        tries = 10
        use_twitter = self.configuration.gather.use_twitter
        use_bonus = self.configuration.gather.use_bonus
        # infinito
        while index < len(rooms) and tries >= 0:
            tries = tries - 1
            timeout = self.showroom_api.get_timeout(rooms[0])
            if timeout is None:
                # get list of items from a valid room, rooms with ballots don't count
                items = self.get_throwable_items(rooms[0], True)
                if len(items) < 5:
                    break

                minimum = 99
                for item in items:
                    if item['free_num'] < minimum and item['gift_id'] != FreeGifts.RAINBOW_STAR.value:
                        minimum = item['free_num']

                if self.configuration.gather.force:
                    minimum = 0

                if minimum < 99:
                    required_bonuses = int((99 - minimum) / 10)
                    required_bonuses = self.configuration.gather.threads \
                                       if self.configuration.gather.threads < required_bonuses \
                                       else required_bonuses

                    if required_bonuses < 1:
                        required_bonuses = 1
                    elif required_bonuses < 2:
                        if self.configuration.gather.overfill:
                            required_bonuses = 2
                            use_bonus = False
                    # FIXME: Solo 2 twitter como maximo
                    else:
                        required_bonuses = 2

                    parallel = Parallel(required_bonuses)
                    for room in rooms:
                        #if required_bonuses > 0 and not (room.badge or room.bonus_checked):
                        #    showroom_manager.lives_manager.refresh(room.live)

                        if required_bonuses > 0:
                            if use_twitter and not room.badge:
                                parallel.add_task(required_bonuses, self.showroom_api.send_tweet, room)
                                required_bonuses -= 1

                        if required_bonuses > 0:
                            if use_bonus and not room.bonus_checked:
                                parallel.add_task(required_bonuses, self.poll_free_gifts,
                                                  room)
                                required_bonuses -= 1

                        if required_bonuses < 1:
                            print(parallel.get_results())
                            break
                else:
                    break
            else:
                log_trace("Bonus embargo til %s" % timeout)
                break

    def do_track(self, filename, rooms):
        """
        Track popularity points for given rooms.
        .params filename: Name of filename where to dump information.
        :type filename: string
        :params rooms: Rooms to check.
        :type rooms: int[]
        """
        try:
            #last = self._load_previous_day(filename)
            last = {}
            active_watch = []
            while True:
                lines = []
                date = datetime.now()
                print(f"Processing {len(rooms)} rooms at {date}...")
                for room_id in rooms:
                    room = self.showroom_manager.rooms_manager.find(room_id)
                    if room is not None:
                        live = self.showroom_manager.showroom_api.get_live_data(room, \
                                   self.showroom_manager.lives_manager)
                        if live != None:
                            line = self._do_track_process_data(room, live, date, last)
                            if line:
                                lines.append(line)

                                if self.configuration.track.save:
                                    savefile = self._do_track_get_filename(date, room)
                                    save_json(live.json, savefile)

                            users = self._do_track_find_official_users(live)
                            if users:
                                print(f"\tIn this arena: {','.join(map(str, users))}.")

                            if self.configuration.track.capture:
                                if live.live_id not in active_watch:
                                    active_watch.append(live.live_id)
                                    self.configuration.watch.capture = True

                                    if room_id != self._KAHOTARU_ROOM_ID:
                                        callback = ReadableBroadcastCallback(self.configuration, room)
                                    else:
                                        callback = WatchBroadcastCallback(self.configuration, room)

                                    self._do_watch_capture(room, callback)

                with open(filename, "a") as output:
                    for line in lines:
                        output.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (line["id"], \
                            line["key"], line["date"], line["actual_date"], line["followers"], \
                            line["viewers"], line["points"], line["diff"]))

                seconds = self.configuration.track.delay - (datetime.now() - date).seconds
                activesleep(seconds)
                self.showroom_manager.initialize()
        except StandardError as err:
            log_error(err)

    def do_hunt_avatars(self, rooms):
        """
        Automatize watching rooms for avatars. Spawn a process for each room.
        :param rooms: List of Room ids.
        :type rooms: int[]
        """
        try:
            while True:
                obtained_rooms = []
                date = datetime.now()
                print(f"Checking {len(rooms)} rooms at {date} for avatars...")
                for room_id in rooms:
                    save = False
                    room = self.showroom_manager.rooms_manager.find(room_id)
                    if room is not None:
                        if not self.configuration.hunt.simulate:
                            live = self.showroom_manager.showroom_api.get_live_data(room, \
                                   self.showroom_manager.lives_manager)

                            if live is not None and not live.is_enquete:
                                respjson = self._do_hunt_avatar(room)
                                if respjson.get("ok"):
                                    save = True
                                    print(f"Obtained avatar from room {str(room_id)}.")
                                else:
                                    if respjson.get('errors'):
                                        print(f"Couldn't obtain avatar from room {room_id} ({respjson['errors'][0].get('error_user_msg')}).")
                            else:
                                print(f"Room {str(room_id)} is in poll mode.")
                        else:
                            print(f"Simulated obtaining avatar from room {str(room_id)}.")

                        if save:
                            obtained_rooms.append(room_id)
                            with open(self.configuration.hunt.target_file, "a") as output:
                                output.write("Tried to obtain avatar from room %s.\n" % str(room_id))

                rooms = [x for x in rooms if x not in obtained_rooms]
                seconds = self.configuration.hunt.delay - (datetime.now() - date).seconds
                activesleep(seconds)
                self.showroom_manager.initialize()
        except StandardError as err:
            log_error(err)

    def do_watch_rooms(self, rooms_id, delay):
        """
        Automatize watching rooms. Spawn a process for each room.
        :param room_id: Room id to watch.
        :type room_id: int
        :param delay: Time to wait between tries.
        :type delay: int
        """
        pids = []
        for room_id in rooms_id:
            pid = os.fork()
            if pid > 0:
                print(f"Spawned process {pid} to watch room {str(room_id)}.")
                pids.append(pid)
            else:
                self.do_watch_room(room_id, delay)
                print(f"Spawned process for room {str(room_id)} ended.")
                os._exit(0)

        while pids:
            pid, status = os.wait()
            print(f"Process {pid} ended with status {status}.")
            pids.remove(pid)

    def do_watch_room(self, room_id, delay):
        """
        Automatize watching a room.
        :param room_id: Room id to watch.
        :type room_id: int
        :param delay: Time to wait between tries.
        :type delay: int
        """
        counted_in_room = self.configuration.watch.skip_count
        japan_tz = timezone('Asia/Tokyo')
        self.configuration.gather.use_twitter = False
        self.configuration.gather.use_bonus = True
        self.configuration.count.delay = 0
        live_id = 0

        while True:
            self._do_watch_wait(room_id, delay)
            print(f"Room {room_id} is online. Refreshing manager...")
            room = self._do_watch_refresh_manager(room_id)

            if room:
                self._do_watch_capture(room)
                while self.showroom_manager.showroom_api.is_online(room_id):
                    self._force_visit(room)

                    print("Refreshing rooms list...")
                    rooms_filter = self.showroom_manager.rooms_manager.create_filter()
                    rooms_filter.official = room.official
                    rooms = self.showroom_manager.rooms_manager.rooms(rooms_filter)

                    if not self.configuration.watch.skip_throw:
                        print("Throwing and reloading items...")
                        self.do_throw_normal_items(room)
                        self.do_reload_items(rooms)
                        self.do_throw_normal_items(room)
                        self.do_reload_items(rooms)
                        self.do_throw_normal_items(room)
                    else:
                        print("Skipping throwing and reloading items...")

                    print("Guessing next round of gathering...")
                    tries = 3
                    timeout = None
                    while tries > 0 and timeout is None:
                        tries -= 1
                        timeout = self.showroom_api.get_timeout(room)
                        if timeout is not None:
                            try:
                                seconds = (japan_tz.localize(datetime.combine(datetime.now().date(), \
                                          datetime.strptime(timeout, "%H:%M:%S").time())) - \
                                          datetime.now(tz=japan_tz)).seconds + 60
                            except StandardError as err:
                                log_error(err)
                                seconds = 600

                    if timeout is None:
                        seconds = 60

                    print(f"Guessed {timeout} (in {seconds} seconds)...")
                    current_date = datetime.now()

                    print("Determining if count is needed...")
                    if live_id != room.live.live_id:
                        counted_in_room = False

                    if not counted_in_room:
                        self._count_in_room(room)
                        counted_in_room = True
                        live_id = room.live.live_id

                    seconds -= (datetime.now() - current_date).seconds
                    if seconds < 1 or seconds > (60 * 60):
                        seconds = 30

                    print(f"Waiting until {timeout} for next round of gathering ({seconds} seconds)...    ")

                    activesleep(seconds, self._do_watch_check_renewal, extra={"room": room})
                    self.showroom_api.clear_timeout(room)
                    print("Woke up! Refreshing room list to gather items...")
                    room = self._do_watch_refresh_manager(room_id)
                    rooms = self.showroom_manager.rooms_manager.rooms(rooms_filter)

                    if not self.configuration.watch.skip_throw:
                        print(f"Found {len(rooms)} rooms. Gathering items...")
                        self.do_reload_items(rooms)
                    else:
                        print(f"Found {len(rooms)} rooms, but skipping gathering items...")

    def get_throwable_items(self, room, normal_items_only=False):
        """Returns array with throwable items in given room."""
        respjson = self.showroom_api.get_current_user(room)
        result = []
        if respjson is not None:
            if respjson['add_free_gift'] == 1:
                print(f"Obtained bonus from room {room.room_id}!")
                room.bonus_checked = True

            result = respjson['gift_list']['enquete'] \
                     if respjson['gift_list']['enquete'] and not normal_items_only \
                     else respjson['gift_list']['normal']

            # Ignore special items in free items
            result = [x for x in result if x['gift_id'] != FreeGifts.RAINBOW_STAR.value]

            if self.configuration.throw.steal_avatar and respjson['gift_list']['enquete']:
                items = [x for x in respjson['gift_list']['normal'] if x['free_num'] > 0]

                if items:
                    result.append({u'free_num': 1, u'gift_id': items[0]['gift_id']})

        return result

    def do_throw_normal_items(self, room, batch=None):
        """
        Throws as many decens of items as possible in given room.
        """
        items = batch if batch is not None and batch \
                else self.get_throwable_items(room)

        # builds an array of throwable items
        throws = []
        for item in items:
            total = item['free_num']

            while total >= self.configuration.throw.step:
                throws.append(
                    {
                        u'gift_id': item['gift_id'], 'free_num': self.configuration.throw.step
                    })
                total -= self.configuration.throw.step

            if total > 0 and self.configuration.throw.everything:
                throws.append({u'gift_id': item['gift_id'], u'free_num': total})

        if not self.configuration.throw.ordered:
            random.shuffle(throws)

        for throw in self._split_array(throws):
            parallel = Parallel(len(throw))

            for element in throw:
                try:
                    PaidGifts(element['gift_id'])
                    function = self._throw_gift
                except ValueError:
                    function = self._throw_item

                parallel.add_task(throw.index(element), function, element['gift_id'],
                                  room.live, element['free_num'])

            print(parallel.get_results())

    def poll_free_gifts(self, room):
        """Polls the room."""
        counter = 0
        result = False

        while counter < 4:
            resp = self.showroom_api.do_polling(room)
            if resp == 0:
                result = True
                break
            elif resp == 1:
                result = False
                break

            counter += 1
            if not result and counter < 4:
                time.sleep(10)

        room.bonus_checked = True
        return result

    def find_room(self, room_id):
        """
        Find the requested room by id.
        :param room_id: Room id to find.
        :type room_id: int
        :returns: Room if found, None if not found.
        :rtype: Room
        """
        #log_trace("Finding room", extra={"room_id": room_id})
        return self.showroom_manager.rooms_manager.find(room_id)

    def do_communication(self, room, callback=None):
        """Logs communication."""
        if callback is None:
            callback = ColoredBroadcastCallback(self.configuration, room)

        showroom_lowlevel_api = ShowroomBroadcast(self.configuration, room, None)
        showroom_lowlevel_api.do_communication(callback)
