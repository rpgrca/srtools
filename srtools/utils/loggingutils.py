"""Standard logging utilities"""
import logging
import inspect
from driftwood.formatters import JSONFormatter

# New trace level for SRTools
_SRTOOLS_TRACE = 25

logging.addLevelName(_SRTOOLS_TRACE, "SRTRACE")
#logging.basicConfig(filename="srtools.log")

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)
_STREAM_HANDLER = logging.StreamHandler()

_FORMATTER = JSONFormatter(extra_attrs=["room_id", "gift_id", "live_id", "num",
                                        "real_pathname", "real_funcname", "real_lineno"])

_STREAM_HANDLER.setFormatter(_FORMATTER)
_LOGGER.addHandler(_STREAM_HANDLER)
_LOGGER.propagate = False

def _srtrace(self, message, *args, **kwargs):
    """Custom tracer."""
    if self.isEnabledFor(_SRTOOLS_TRACE):
        self.log(_SRTOOLS_TRACE, message, *args, **kwargs)

logging.Logger.srtrace = _srtrace

def _merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def _inject_location(**kwargs):
    """
    Injects the frame location
    :param kwargs: List of arguments.
    """
    func = inspect.currentframe().f_back.f_back.f_code
    extra = {
        "real_lineno": func.co_firstlineno,
        "real_pathname": func.co_filename,
        "real_funcname": func.co_name
    }

    if "extra" in kwargs:
        #kwargs["extra"] = _merge_dicts(kwargs['extra'], extra)
        kwargs.update({"extra": _merge_dicts(kwargs["extra"], extra)})
    else:
        kwargs.update({"extra": extra})
        #kwargs["extra"] = extra

    return kwargs

def log_trace(*args, **kwargs):
    """
    Write formatted text to log facility, trace level.
    :param args: Format
    :param kwargs: Arguments
    """
    new_kwargs = _inject_location(**kwargs)
    _LOGGER.srtrace(*args, **new_kwargs)

def log_debug(*args, **kwargs):
    """
    Write formatted text to log facility, debug level.
    :param args: Format
    :param kwargs: Arguments
    """
    new_kwargs = _inject_location(**kwargs)
    _LOGGER.debug(*args, **new_kwargs)

def log_error(*args, **kwargs):
    """
    Write formatted text to log facility, error level.
    :param args: Format
    :param kwargs: Arguments
    """
    new_kwargs = _inject_location(**kwargs)
    _LOGGER.error(*args, **new_kwargs)
