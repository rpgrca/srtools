# srtools
A set of command-line utilities to interact with the showroom-live.com web api (unofficial).

## Usage examples
Room id refers to the room id which is usually found in the broadcaster's profile room (for example, https://www.showroom-live.com/room/profile?room_id=10). For some commands it's possible to supply an alias defined in srtools/resources/fav_user.json. Not all options per command nor every command is listed here.

### Check if room is online
    main.py online [room id]
    > Room [room id] is not online
    > Room [room id] is online

### Track rooms
    main.py track -r 48g -c -s -d 60
    -r: list of comma-separated room ids, or a group alias defined in srtools/resources/fav_group.json
    -c: capture the communication in the room
    -s: saves information captured with the -c switch to a file.
    -d: delay between checks for rooms to become online in seconds
    
### Count from 1 to 50 in room
    main.py count -s 1 -e 50 [room id]
    -s: starting value (default: 1)
    -e: ending value (default: 50)

### Gather stars (from official rooms) / seeds (from amateur rooms)
    main.py gather -t 2 -u official/amateur
    -t: amount of threads to use (default: 20 but 2 is optimal)
    -u: visit rooms and stay there for 30 seconds to see if bonus is gathered.

### Throw free gifts in room (stars in official rooms, seeds in amateur rooms)
    main.py throw [room id]

### Throw paid gifts in rooms
    main.py throw -i HEART=100 -s 10 -t 10 [room id]
    -i: list of comma-separated items to throw with their amounts
    -s: throw in group of 10 items to get 20% bonus
    -t: amount of threads to use
    
### Send a message to a room
    main.py message [room id] -m "Message"
    -m: Message to send. Will mark the room as visited.
    
### Change name and/or avatar
    main.py profile -a [avatar id] -n [new name]
    -a: avatar id, must be in user's list of avatars
    -n: new name to choose
    It's possible to change more attributes but these two must always be supplied.
    
## Version 2.0
- Runs (tested) on Python 3.9.5.
- In order to make it run it's necessary to login using Firefox to www.showroom-live.com, then edit the source code of the HTML, extract the CSRF token and add it to line 21 in srtools/manager/api/callbacks/showroomwebservice.py.
- If it cannot discover the cookies it'll be necessary to decompress the session files for browsercookie to handle it. Once you find the cookie file (sessionstore-backup/recovery.jsonlz4 for example) follow [these steps](https://gist.github.com/jscher2000/07f94249b0a5f6d565fb20d88b73bb91) for Firefox <66 or [these](https://gist.github.com/jscher2000/4403507e33df0918289619edb83f8193) for Firefox+66.
- Verify what hasn't been implemented from the [API](https://qiita.com/takeru7584/items/f4ba4c31551204279ed2) and from the [live communication](https://seesaawiki.jp/shokoro/d/%c4%cc%bf%ae%ca%fd%cb%a1).

Uses modified versions of browsercookie and driftwood:
- [browsercookie](https://github.com/richardpenman/browsercookie): cookie parser exits after parsing a .js file instead of next parsing the Mozilla version (since it crashed on me).
- [driftwood](https://github.com/gitter-badger/driftwood): modifications to make it compatible with Python 2.7

### Disclaimer
Misuse might lead to account banning, I'm not responsible. This started as a personal practice to use Python to interact with a web api on July 2017 and has little changed I reached what I wanted to do, a few months later. Just small modifications have been done since then (after Showroom removed the ability to gather free items by tweeting, for example). It's also not user friendly, nor it's supposed to at this point, for better alternatives check [Shokoro](https://seesaawiki.jp/shokoro/), [Sukosuko Tool](https://chrome.google.com/webstore/detail/showroom-%E3%81%99%E3%81%93%E3%81%99%E3%81%93%E3%83%84%E3%83%BC%E3%83%AB%EF%BC%8B/bpimjnbkllaejbmjhceepgndkdapnafd?h1=en), [Chokotto Tool](https://greasyfork.org/en/scripts/393234-showroom-%E3%81%A1%E3%82%87%E3%81%93%E3%81%A3%E3%81%A8%E3%83%84%E3%83%BC%E3%83%AB), etc.
