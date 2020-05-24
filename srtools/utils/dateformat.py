"""Formats date/time."""
import datetime

def formatted_date(date=None, include_milliseconds=False):
    """
    Return formatted date.
    :param date: Date to convert.
    :type date: datetime.datetime
    :returns: Formatted date in format "YYYYMMDD-HHMMSS".
    :rtype: string
    """

    if date is None:
        date = datetime.datetime.now()

    if include_milliseconds:
        dateformat = "%Y%m%d-%H%M%S%f"
    else:
        dateformat = "%Y%m%d-%H%M%S"

    return date.strftime(dateformat)
