"""Configuration class."""
import os.path
from abc import ABCMeta, abstractmethod
from enum import Enum
from srtools.utils.jsonutils import load_json, save_json

class FavoriteConfigSupport(object):
    """Base support for favorites configuration."""
    __metaclass__ = ABCMeta

    RESOURCES_DIR = None
    CONFIGURATION_FILE = None
    filename = None
    favorites = None
    favorites_set = None

    def __init__(self):
        if os.path.exists('srtools/resources'):
            self.RESOURCES_DIR = 'srtools/resources'
        else:
            self.RESOURCES_DIR = 'resources'

        self.filename = os.path.join(self.RESOURCES_DIR, self.CONFIGURATION_FILE)
        self.favorites = {}

    def __getitem__(self, key):
        return self.favorites[key]

    def __contains__(self, item):
        return item in self.favorites

    def __iter__(self):
        return self.favorites.iterkeys()

    @abstractmethod
    def reset(self):
        """Reset favorite configuration."""
        pass

    def load(self):
        """
        Load the avatar list. If no file found, use internal default.
        """
        respjson = load_json(self.filename)
        if respjson is not None:
            self.favorites = respjson
        else:
            self.reset()

    def save(self):
        """
        Save the current avatar list.
        """
        save_json(self.favorites, self.filename)

class FavoriteAvatarsConfiguration(FavoriteConfigSupport):
    """Favorite avatars configuration."""
    CONFIGURATION_FILE = 'fav_avatar.json'

    def __init__(self):
        super(FavoriteAvatarsConfiguration, self).__init__()
        self.load()
        self.favorites_set = set(self.favorites.values())

    def reset(self):
        """Resets favorite avatars configuration."""
        self.favorites = {
            'dragon'   : 1002885,
            'ship'     : 1002818,
            'shimada'  : 1002954,
            'kujira'   : 1001899,
            'kurage'   : 1002425,
            'kurenyan' : 1002911,
            'kurenyan2': 1002843,
            'kurano'   : 1002657,
            'yoshi'    : 1002586,
            'phoenix'  : 85
        }

class FavoriteUsersConfiguration(FavoriteConfigSupport):
    """Favorite users configuration."""
    CONFIGURATION_FILE = 'fav_user.json'

    def __init__(self):
        super(FavoriteUsersConfiguration, self).__init__()
        self.load()
        self.favorites_set = set(self.favorites.values())

    def reset(self):
        """Resets favorites configuration."""
        self.favorites = {
            'an'       :  62104,
            'dai'      :  89528,
            'kuro'     :  72070,
            'yoshi'    :  89619,
            'narita'   :  78582,
            'harunyan' :  48576,
            'momo'     :  71559,
            'kokoro'   :  68422,
            'kohachan' :  76524,
            'ryuu'     :  88328,
            'sensei'   :  84165,
            'aya'      :  29158,
            'katsukun' : 104074,
            'tsukushi' :  94952,
            'chankana' :  74646,
            'tsubasa'  :  37456,
            'yukina'   :  67019,
            'shiitan'  :  24798,
            'piyomaru' :  61575,
            'arichan'  :  80501,
            'prada'    :  82269,
            'kabo'     :  87239,
            'kahotaru' :  97203,
            'kurumin'  :  97446,
            'choppa'   :  76933,
            'irisama'  : 107501,
            'takabon'  : 101035,
            'ann'      :  69351,
            'nono'     :  71490,
            'mecha'    : 100001,
            'mecha2'   : 116886,
            'mao'      :  36894,
            'masataru' :  92574,
            'yuuni'    :  80088,
            'aina'     :  92401,
            'ayapon'   :  18998,
            'rea'      :  68735,
            'stu48_official': 109060
        }

class FavoriteOfficialUsersConfiguration(FavoriteConfigSupport):
    """Favorite 46/48 users configuration."""
    CONFIGURATION_FILE = 'fav_official_users.json'

    def __init__(self):
        super(FavoriteOfficialUsersConfiguration, self).__init__()
        self.load()
        self.favorites_set = set(self.favorites.keys())

    def reset(self):
        """Resets favorite official users configuration."""
        self.favorites = {}

class FavoriteGroupsConfiguration(FavoriteConfigSupport):
    """."""
    CONFIGURATION_FILE = 'fav_group.json'

    def __init__(self):
        super(FavoriteGroupsConfiguration, self).__init__()
        self.load()
        self.favorites_set = set(self.favorites["48g"])

    def reset(self):
        """Resets groups configuration."""
        # wget "https://www.showroom-live.com/campaign/all_rooms?title=akb48_sr&group=ngt48" --quiet -O-| grep "room_id" | sed -e 's/.*room_id=\([^"]*\)".*/\1/g' | sort
        #      --quiet -O-| grep "room_id" | sed -e 's/.*room_id=\([^"]*\)".*/\1/g' | sort
        self.favorites = {
            "stu48" : [
                96992, 96993, 96999, 97002, 97011, 97165, 97168, 97169, 97170, 97172,
                97176, 97189, 97192, 97194, 97203, 97212, 97213, 97429, 97431, 97432,
                97433, 97439, 97440, 97441, 97442, 97446, 99665, 99668, 99671, 99672,
                99675
            ],
            "ngt48" : [
                61707, 61710, 61711, 61712, 61713, 61719, 61720, 61721, 61722, 61723,
                61724, 61725, 61726, 61727, 61728, 61729, 61730, 61731, 61732, 61733,
                61734, 61736, 61884, 61885
            ],
            "hkt48" : [
                61701, 61702, 61703, 61704, 61705, 61706, 61765, 61766, 61767, 61768,
                61770, 61771, 61772, 61773, 61774, 61775, 61776, 61777, 61778, 61780,
                61781, 61782, 61784, 61785, 61786, 61787, 61788, 61789, 61790, 61791,
                61792, 61793, 61794, 61795, 61796, 61798, 61799, 61800, 61801, 61802,
                79288, 79289, 79296, 79297, 79298, 79299, 79300, 79301, 79302, 79303
            ],
            "nmb48" : [
                61739, 61740, 61741, 61742, 61743, 61744, 61745, 61747, 61749, 61750,
                61751, 61753, 61754, 61755, 61759, 61760, 61761, 61762, 61763, 61764,
                61856, 61857, 61858, 61859, 61861, 61862, 61863, 61864, 61865, 61866,
                61867, 61868, 61869, 61871, 61872, 61873, 61874, 61875, 61876, 61877,
                61878, 61879, 61880, 67800, 67801, 69434, 69435, 69436, 69437, 69438,
                69439, 69440, 69441, 69442, 69443
            ],
            "ske48" : [
                61566, 61569, 61571, 61573, 61577, 61581, 61591, 61593, 61595, 61675,
                61676, 61677, 61678, 61679, 61680, 61682, 61683, 61684, 61814, 61816,
                61817, 61818, 61819, 61821, 61822, 61823, 61824, 61830, 61832, 61833,
                61834, 61836, 61837, 61838, 61840, 61841, 61842, 61843, 61844, 61845,
                61847, 61848, 61849, 61852, 61853, 61854, 61855, 61882, 61883, 67790,
                67792, 67794, 67795, 67796, 76498, 76501, 76503, 76505, 76511, 76518,
                76523, 76524, 76535, 76539, 76542, 76549, 76550, 76553, 76554, 76556,
                76760,
            ],
            "akb48" : [
                109423, 61528, 61529, 61530, 61532, 61533, 61534, 61535, 61537, 61538,
                61539, 61540, 61543, 61544, 61545, 61546, 61547, 61548, 61549, 61550,
                61551, 61552, 61553, 61554, 61555, 61556, 61557, 61559, 61560, 61561,
                61562, 61563, 61564, 61565, 61567, 61568, 61570, 61572, 61574, 61576,
                61578, 61580, 61582, 61583, 61584, 61585, 61587, 61588, 61589, 61590,
                61592, 61594, 61596, 61601, 61602, 61603, 61604, 61609, 61610, 61611,
                61612, 61613, 61614, 61615, 61617, 61618, 61619, 61621, 61622, 61626,
                61627, 61628, 61629, 61630, 61631, 61632, 61633, 61634, 61636, 61637,
                61638, 61639, 61641, 61645, 61737, 61804, 61805, 61806, 61807, 61809,
                61810, 61811, 61812, 67783, 67784, 67785, 67786, 67787, 67788, 67789,
                92039, 92040, 92041, 92042, 92043, 92044, 92045, 92046, 92048, 92050,
                92052, 92053, 92054, 92055, 92056, 92057, 92058, 92059, 96769, 96770,
            ]
        }
        self.favorites["48g"] = self.favorites["akb48"] + self.favorites["ske48"] + \
                                self.favorites["nmb48"] + self.favorites["hkt48"] + \
                                self.favorites["ngt48"] + self.favorites["stu48"]

class HuntedAvatarsConfiguration(FavoriteConfigSupport):
    """Favorite avatars configuration."""
    CONFIGURATION_FILE = 'hunting.json'

    def __init__(self):
        super(HuntedAvatarsConfiguration, self).__init__()
        self.load()
        self.hunted_avatars = set(self.favorites["hunting"])

    def reset(self):
        """Resets hunting configuration."""
        self.favorites = {
            "hunting" : []
        }

class ObtainedAvatarsConfiguration(FavoriteConfigSupport):
    """Obtained avatars configuration."""
    CONFIGURATION_FILE = 'obtained_avatars.json'

    def __init__(self):
        super(ObtainedAvatarsConfiguration, self).__init__()
        self.load()
        self.avatars = set(self.favorites["avatars"])

    def reset(self):
        self.favorites = {
            "avatars": []
        }

"""
---
"""
class SelectedConfiguration(Enum):
    """Current selected configuration."""
    UNDEFINED = 0
    GATHER = 1
    THROW = 2
    COUNT = 3
    ONLINE = 4
    PROFILE = 5
    WATCH = 6
    LOTTERY = 7
    TEST = 8
    TRACK = 9
    LIST_AVATARS = 10
    LIST_USERS = 11
    LIST_GROUPS = 12
    CAPTURE = 13
    MESSAGE = 14
    HUNT = 15
    STALK = 16

class PaidGifts(Enum):
    """Paid gifts ids."""
    RED_DARUMA = 4
    YELLOW_DARUMA = 1101
    PURPLE_DARUMA = 1102
    GREEN_DARUMA = 1103
    BLUE_DARUMA = 1104
    HEART = 3
    ROSE = 5
    COIN = 6
    SAKURA = 20039
    RACIMO = 7
    FUROSHIKI = 8
    IINE = 11
    TAKO = 12
    ICECREAM = 13
    VALENTINE_HEART = 2037
    VALENTINE_CHOCO = 2038
    WHITE_VALENTINE_CHOCO = 2041
    DARUMA_FACE = 700045
    DARUMA_CAN = 700046
    AKB_MAMORI = 600028
    STU_MAMORI = 600033

class ClassicFreeGifts(Enum):
    YELLOW_STAR = 1
    RED_STAR = 1001
    PURPLE_STAR = 1002
    GREEN_STAR = 1003
    BLUE_STAR = 2
    YELLOW_SEED = 1501
    RED_SEED = 1502
    PURPLE_SEED = 1503
    GREEN_SEED = 1504
    BLUE_SEED = 1505

class FreeGifts(Enum):
    """Free gift Ids"""
    YELLOW_STAR = ClassicFreeGifts.YELLOW_STAR.value
    RED_STAR = ClassicFreeGifts.RED_STAR.value
    PURPLE_STAR = ClassicFreeGifts.PURPLE_STAR.value
    GREEN_STAR = ClassicFreeGifts.GREEN_STAR.value
    BLUE_STAR = ClassicFreeGifts.BLUE_STAR.value
    RAINBOW_STAR = 1601
    YELLOW_SEED = ClassicFreeGifts.YELLOW_SEED.value
    RED_SEED = ClassicFreeGifts.RED_SEED.value
    PURPLE_SEED = ClassicFreeGifts.PURPLE_SEED.value
    GREEN_SEED = ClassicFreeGifts.GREEN_SEED.value
    BLUE_SEED = ClassicFreeGifts.BLUE_SEED.value
    UNKNOWN_FREE_GIFT = 2309
    UNKNOWN_FREE_GIFT_2 = 2311

class BallotGifts(Enum):
    """Free ballot Ids"""
    BALLOT_01 = 10001
    BALLOT_02 = 10002
    BALLOT_03 = 10003
    BALLOT_04 = 10004
    BALLOT_05 = 10005
    BALLOT_06 = 10006
    BALLOT_07 = 10007
    BALLOT_08 = 10008
    BALLOT_09 = 10009
    BALLOT_10 = 10010
    BALLOT_11 = 10011
    BALLOT_12 = 10012
    BALLOT_13 = 10013
    BALLOT_14 = 10014
    BALLOT_15 = 10015
    BALLOT_16 = 10016
    BALLOT_17 = 10017
    BALLOT_18 = 10018
    BALLOT_19 = 10019
    BALLOT_20 = 10020
    BALLOT_21 = 10021
    BALLOT_22 = 10022
    BALLOT_23 = 10023
    BALLOT_24 = 10024
    BALLOT_25 = 10025

"""
---
"""
class DaemonConfiguration(object):
    """Daemon configuration."""
    def __init__(self):
        self.reset()

    def reset(self):
        """Resets daemon configuration."""
        self.loop = False
        self.countdown = 0

class TestConfiguration(object):
    """Test configuration."""
    def __init__(self):
        self.reset()

    def reset(self):
        """Resets test configuration."""
        self.target_room = None

class ConnectionConfiguration(object):
    """Connection configuration."""
    def __init__(self):
        self.reset()

    def reset(self):
        """Resets connection information."""
        self.cookies = "firefox"
        self.timeout = 30
        self.retries = 3
        self.debug = False
        self.user_agent = \
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0'
            #'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'

class GatherConfiguration(object):
    """Gather configuration."""
    def __init__(self):
        self.reset()

    def reset(self):
        """Resets gather configuration."""
        self.threads = 20
        self.use_twitter = False
        self.use_bonus = False
        self.official = True
        self.overfill = False
        self.force = False

class OnlineConfiguration(object):
    """Online checker configuration."""
    def __init__(self):
        self.reset()

    def reset(self):
        """Resets online configuration."""
        self.target_room = None
        self.verbose = False

class LotteryConfiguration(object):
    """Lottery configuration."""
    def __init__(self):
        self.reset()

    def reset(self):
        """Resets lottery configuration."""
        self.name = None
        self.target = 0

class ThrowConfiguration(object):
    """Throw configuration."""
    def __init__(self):
        self.reset()

    def reset(self):
        """Resets throw configuration."""
        self.threads = 4
        self.target_room = -1
        self.everything = False
        self.force = False
        self.step = 10
        self.ordered = False
        self.items = {}
        self.steal_avatar = False

class CaptureConfiguration(object):
    """Capture configuration."""
    def __init__(self):
        self.reset()

    def reset(self):
        """Resets capture configuration."""
        self.target_room = -1
        self.output = "stdout"
        self.type = "colored"

class TrackConfiguration(object):
    """Track configuration."""
    def __init__(self):
        self.reset()

    def reset(self):
        """Resets track configuration."""
        self.target_rooms = {}
        self.delay = 300
        self.save = False
        self.target_file = "track.txt"
        self.capture = False

class HuntConfiguration(object):
    """Hunt configuration."""
    def __init__(self):
        self.reset()

    def reset(self):
        """Resets hunting configuration."""
        self.delay = 30
        self.target_file = "avatar.txt"
        self.target_rooms = "hunting"
        self.simulate = False

class StalkConfiguration(object):
    """Stalk configuration."""
    def __init__(self):
        self.reset()

    def reset(self):
        """Resets stalking configuration."""
        self.delay = 30
        self.target_file = "stalked_avatar.txt"
        self.target_rooms = {}
        self.simulate = False

class WatchConfiguration(object):
    """Watch configuration."""
    def __init__(self):
        self.reset()

    def reset(self):
        """Resets watch configuration."""
        self.delay = 10
        self.skip_count = False
        self.skip_throw = False
        self.target_room = -1
        self.capture = False

class LoginConfiguration(object):
    """Login configuration."""
    def __init__(self):
        self.reset()

    def reset(self):
        """Resets login configuration."""
        self.username = ""
        self.password = ""
        self.captcha_word = ""

class ListConfiguration(object):
    """List configuration."""
    def __init__(self):
        self.reset()

    def reset(self):
        """Resets list configuration."""
        self.list = ""

class CountConfiguration(object):
    """Count configuration."""
    def __init__(self):
        self.reset()

    def reset(self):
        """Resets count configuration."""
        self.target_room = -1
        self.threads = 1
        self.message = None
        self.minimum_live_id = 0
        self.delay = 1.25
        self.start = 1
        self.end = 50
        self.max_tries = 5
        self.no_visit = False
        self.repeat = 1
        self.skip = []

class MessageConfiguration(object):
    """Message configuration."""
    def __init__(self):
        self.reset()

    def reset(self):
        """Resets message configuration."""
        self.target_room = -1
        self.message = None
        self.max_tries = 5
        self.no_visit = False

class ProfileConfiguration(object):
    """Profile configuration."""
    def __init__(self):
        self.reset()

    def reset(self):
        """Resets profile configuration."""
        self.token = "O4rGyVGGHOJhSCTFTcrQbDDt6q5JTwFBwTaU2xRo"
        self.name = None
        self.trim_left = None
        self.trim_top = None
        self.trim_right = None
        self.trim_bottom = None
        self.trim_width = None
        self.trim_height = None
        self.trim_origin_width = None
        self.trim_origin_height = None
        self.profile_image = None
        self.avatar_id = None
        self.description = None

class Configuration(object):
    """Configuration object."""
    def __init__(self):
        self.gather = GatherConfiguration()
        self.throw = ThrowConfiguration()
        self.count = CountConfiguration()
        self.online = OnlineConfiguration()
        self.favorite_official_users = FavoriteOfficialUsersConfiguration()
        self.favorite_users = FavoriteUsersConfiguration()
        self.favorite_avatars = FavoriteAvatarsConfiguration()
        self.favorite_groups = FavoriteGroupsConfiguration()
        self.obtained_avatars = ObtainedAvatarsConfiguration()
        self.hunted_avatars = HuntedAvatarsConfiguration()
        self.profile = ProfileConfiguration()
        self.daemon = DaemonConfiguration()
        self.connection = ConnectionConfiguration()
        self.login = LoginConfiguration()
        self.watch = WatchConfiguration()
        self.lottery = LotteryConfiguration()
        self.track = TrackConfiguration()
        self.test = TestConfiguration()
        self.capture = CaptureConfiguration()
        self.message = MessageConfiguration()
        self.hunt = HuntConfiguration()
        self.stalk = StalkConfiguration()
        self.reset()

    def reset(self):
        """Resets configuration."""
        self.chosen = SelectedConfiguration.UNDEFINED
        self.gather.reset()
        self.throw.reset()
        self.count.reset()
        self.online.reset()
        self.daemon.reset()
        self.profile.reset()
        self.connection.reset()
        self.login.reset()
        self.watch.reset()
        self.lottery.reset()
        self.test.reset()
        self.capture.reset()
        self.message.reset()
        self.hunt.reset()
        self.stalk.reset()
        # Favorite configurations load automatically from file
        #self.favorite_official_users.reset()
        #self.favorite_users.reset()
        #self.favorite_avatars.reset()
        #self.favorite_groups.reset()
        #self.hunted_avatars.reset()
