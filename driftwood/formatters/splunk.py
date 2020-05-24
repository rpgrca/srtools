import json

from .json import JSONFormatter

class SplunkFormatter(JSONFormatter):
    """Formats messages as JSON with order preserved for splunk

    Accepts the same arguments as :class:`~driftwood.formatters.json.JSONFormatter`
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("preserve_order", True)
        kwargs.setdefault("specific_order", ["created"])
        kwargs.setdefault("regular_attrs", 
            [
                "created", "levelname", "message", "pathname",
                "lineno", "funcName", "process", "levelno"
            ]
        )
        super().__init__(*args, **kwargs)
