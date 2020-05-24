"""Error output."""
from __future__ import print_function
import sys
# import logging

# SRTOOLS_TRACE = 25
# logging.addLevelName(SRTOOLS_TRACE, "SRTools Trace")

# logging.basicConfig(level=SRTOOLS_TRACE)
# LOGGER = logging.getLogger(__name__)

# def _srtrace(self, message, *args, **kwargs):
#     """Custom tracer."""
#     if self.isEnabledFor(SRTOOLS_TRACE):
#         self.log(SRTOOLS_TRACE, message, args, **kwargs)

# logging.Logger.srtrace = _srtrace

def print_error(*args, **kwargs):
    """
    Write formatted text to standard error.
    :param args: Format
    :param kwargs: Arguments
    """
    print(*args, file=sys.stderr, **kwargs)
    #LOGGER.error(*args, **kwargs)

# def print_info(*args, **kwargs):
#     """
#     Write formatted text to log facility.
#     :param args: Format
#     :param kwargs: Arguments
#     """
#     #LOGGER.info(*args, **kwargs)
#     LOGGER.srtrace(*args, **kwargs)

# def print_debug(*args, **kwargs):
#     """
#     Write formatted debug text to log facility.
#     :param args: Format
#     :param kwargs: Arguments
#     """
#     LOGGER.debug(*args, **kwargs)
