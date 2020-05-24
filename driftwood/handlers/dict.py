import logging

from driftwood.formatters import DictFormatter

class DictHandler(logging.Handler):
    """Formats log records into a dict.

    Meant to be subclassed.  
    This is just a convenience wrapper around :py:class:`driftwood.formatters.dict.DictFormatter`.
    """
    def __init__(self, *args, regular_attrs=None, extra_attrs=[], **kwargs):
        """
        :param list extra_attrs: String names of extra attributes that may exist on the log record.
        """
        super().__init__(*args, **kwargs)
        self._dict_formatter = DictFormatter(regular_attrs=regular_attrs,
            extra_attrs=extra_attrs)

    def emit(self, record):
        """Super this in your subclass to format the record into a dict"""
        return self._dict_formatter.format(record)
