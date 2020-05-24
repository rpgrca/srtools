import logging

import mongoengine

from .dict import DictHandler

class BaseLogRecord(mongoengine.Document):
    """Template for log records.

    Allows subclassing to create your own log record document
    if you will be logging extra attributes.
    """
    meta = {'allow_inheritance': True, 'abstract': True}
    msecs = mongoengine.FloatField()
    name = mongoengine.StringField(required=True)
    levelname = mongoengine.StringField()
    pathname = mongoengine.StringField()
    process = mongoengine.IntField()
    lineno = mongoengine.IntField()
    relativeCreated = mongoengine.FloatField()
    funcName = mongoengine.StringField()
    created = mongoengine.FloatField()
    message = mongoengine.StringField(required=True)
    threadName = mongoengine.StringField()
    filename = mongoengine.StringField()
    levelno = mongoengine.IntField()
    thread = mongoengine.LongField()
    module = mongoengine.StringField()

class LogRecord(BaseLogRecord):
    """
    Is used as the default document for log records.

    May not be sublassed.
    """
    pass

class MongoHandler(DictHandler):
    """A handler that will log to MongoDB for you."""
    def __init__(self, *args, document=LogRecord, **kwargs):
        """
        :param mongoengine.Document document: The document that should be used for storing log messages.
            Defaults to :class:`~driftwood.handlers.mongo.LogRecord`.
            If you are using extra_attrs parameter of :class:`~driftwood.handlers.dict.DictHandler`,
            you must define your own document.

        Additionally accepts the same arguments as :class:`~driftwood.handlers.dict.DictHandler`
        """
        super().__init__(*args, **kwargs)
        self.document = document

    def emit(self, record):
        """Converts the log record into a mongoengine document and saves it.

        You can subclass and override this to do neat things.
        """
        msg_dict = super().emit(record)
        log_doc = self.document()
        for msg_key, msg_value in msg_dict.items():
            setattr(log_doc, msg_key, msg_value)
        log_doc.save()
