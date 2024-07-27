from collections.abc import Iterable
from abc import ABCMeta
import re

class Singleton(ABCMeta):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = object.__new__(cls, *args, **kwargs)
            cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]

# Equivalent to any(), without short-circuiting
def any_nsc(it: Iterable) -> bool:
    result = False
    for a in it:
        result |= bool(a)
    return result

def unescape(s: str, encoding: str = 'utf-8') -> str:
    return s.encode('latin1').decode('unicode-escape').encode('latin1').decode(encoding)

def full_unescape(s: str) -> str:
    while '\\' in s:
        try:
            s = unescape(s)
        except UnicodeDecodeError:
            return s
    return s
