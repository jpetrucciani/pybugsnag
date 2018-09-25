"""
text manipulation utilities
"""
import re
from datetime import datetime


DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
DATE_FORMAT_MILLIS = "%Y-%m-%dT%H:%M:%S.%fZ"
FIRST_CAP = re.compile("(.)([A-Z][a-z]+)")
ALL_CAP = re.compile("([a-z0-9])([A-Z])")
LOCALS_FILTER = ["self", "kwargs"]


def snakeify(text):
    """camelCase to snake_case"""
    first_string = FIRST_CAP.sub(r"\1_\2", text)
    return ALL_CAP.sub(r"\1_\2", first_string).lower()


def filter_locals(local_variables, extras=None):
    """filters out builtin variables in the local scope and returns locals as a dict"""
    var_filter = LOCALS_FILTER.copy()
    if extras and isinstance(extras, list):
        var_filter += extras
    return {
        x: local_variables[x]
        for x in local_variables
        if local_variables[x] is not None and x not in var_filter
    }


def datetime_to_iso8601(date_object, milliseconds=False):
    """converts a datetime to the time format bugsnag wants"""
    return date_object.strftime(DATE_FORMAT_MILLIS if milliseconds else DATE_FORMAT)


def iso8601_to_datetime(date_string, milliseconds=False):
    """converts a iso8601 string to a python datetime"""
    return datetime.strptime(
        date_string, DATE_FORMAT_MILLIS if milliseconds else DATE_FORMAT
    )


def dict_to_query_params(params):
    """given a dictionary of query params, form the query param string"""
    if not params:
        return ""
    for param in params:
        if isinstance(params[param], bool):
            params[param] = str(params[param]).lower()
        elif isinstance(params[param], datetime):
            params[param] = datetime_to_iso8601(params[param])
    return "?{}".format("&".join(["{}={}".format(x, params[x]) for x in params]))
