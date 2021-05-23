"""Json utilities."""
import json
from srtools.utils.loggingutils import log_error

def load_json(filename):
    """
    Load a json file.
    :param filename: Name of file to load.
    :type filename: string
    :returns: Json object if loaded, None if not.
    :rtype: string
    """
    filejson = None
    try:
        with open(filename, 'r') as inputfile:
            filejson = json.load(inputfile)
    except Exception as err:
        log_error(err)

    return filejson

def save_json(dictionary, filename):
    """
    Save a dictionary into a json file.
    :param dictionary: Dictionary to save.
    :type dictionary: Dictionary
    :param filename: Name of the file to save.
    :type filename: string
    """
    try:
        text = json.dumps(dictionary, indent=4, sort_keys=True)
        with open(filename, 'w') as outfile:
            outfile.write(text)
    except Exception as err:
        log_error(err)
