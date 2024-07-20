from collections.abc import Iterable

# Equivalent to any(), without short-circuiting
def any_nsc(it: Iterable):
    result = False
    for a in it:
        result |= bool(a)
    return result
