""""""
from srtools.configuration.configuration import FreeGifts, PaidGifts, BallotGifts

_FREE_GIFTS_VALUES = [item.value for item in FreeGifts]
_PAID_GIFTS_VALUES = [item.value for item in PaidGifts]
_BALLOT_VALUES = [item.value for item in BallotGifts]

def throwable_item_name(enum_id):
    """Convert enum id into enum name."""
    result = enum_id

    if enum_id in _FREE_GIFTS_VALUES:
        result = FreeGifts(enum_id).name
    elif enum_id in _PAID_GIFTS_VALUES:
        result = PaidGifts(enum_id).name 
    elif enum_id in _BALLOT_VALUES:
        result = BallotGifts(enum_id).name

    return result
