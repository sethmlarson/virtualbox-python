import sys


PY3 = sys.version_info[0] >= 3

try:
    STRING_TYPES = (unicode,)
    BINARY_TYPES = (bytes, str)
except NameError:
    STRING_TYPES = (str,)
    BINARY_TYPES = (bytes,)


def to_bytes(x):
    if isinstance(x, STRING_TYPES):
        return x.encode("utf-8")
    return x


def to_str(x):
    if isinstance(x, BINARY_TYPES):
        return x.decode("utf-8")
    return x
