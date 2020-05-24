from .dict import DictHandler

__all__ = ["DictHandler"]

try:
    from .mongo import MongoHandler
    __all__.append(MongoHandler)
except:
    #Allow people to use this without mongoengine installed
    pass
