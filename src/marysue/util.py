# encoding: UTF-8

import string
import sys
import random


# ...stolen from seedbank https://github.com/catseye/seedbank/ ...
def autoseed():
    from datetime import datetime
    import os
    import sys

    base_filename = 'seedbank.log'
    filename = os.path.join(os.getenv('HOME'), base_filename)
    if not os.path.exists(filename):
        filename = base_filename

    seed_ = os.getenv('SEEDBANK_SEED', None)
    if seed_ == 'LAST':
        with open(filename, 'r') as f:
            for line in f:
                pass
            seed_ = int(line.split(':')[-1].strip())
    try:
        seed_ = int(seed_)
    except TypeError:
        seed_ = None
    if seed_ is None:
        seed_ = random.randint(0, 1000000)

    with open(filename, 'a') as f:
        f.write('%s: %s: %s\n' % (sys.argv[0], datetime.now(), seed_))
    random.seed(seed_)
    return seed_

autoseed()


# - - - -


def chance(percent, obj=True):
    return obj if random.randint(1, 100) <= percent else None


def lowercase():
    return random.choice(string.lowercase)


def extract(v, filter=lambda x: True):
    """Given a `set` of values `v`, randomly select a value from `v`,
    remove it from `v` (changing `v` as a side-effect), and return it.
    Only values for which the `filter` is true are considered.
    If `v` is empty or no values in `v` qualify for the filter, `v`
    is not modified and the function returns None."""

    z = [x for x in v if filter(x)]
    if not z:
        return None
    p = random.choice(z)
    v.remove(p)
    return p


class ShuffleDemon(object):
    """
    https://www.youtube.com/watch?v=KZnLjRi_g9o
    https://www.youtube.com/watch?v=q6_sLmuze98

    """

    def __init__(self):
        self.registry = {}
        self.enabled = True

    def choice(self, tup):

        if not self.enabled:
            return random.choice(tup)

        if tup not in self.registry:
            #log(repr(tup))
            self.registry[tup] = set()

        if not self.registry[tup]:
            self.registry[tup] = set(tup)

        return extract(self.registry[tup])


shuffle_demon = ShuffleDemon()


def choice(v):
    if isinstance(v, set):
        v = tuple(v)
    return random.choice(v)


def _choice(v):
    """This variant of Python's `random.choice` is enhanced to allow it to
    operate on `set`s, and to allow it to use the ShuffleDemon when
    it works on tuples."""

    from marysue.objects import Object, Group   # sigh!!!
    from marysue.ast import AST
    if isinstance(v, set):
        return random.choice(tuple(v))
    if isinstance(v, Group):
        return random.choice(v)

    assert isinstance(v, tuple), repr(v) + ' ... ' + v.__class__.__name__
    for i in v:
        assert isinstance(
            i, (basestring, Object, AST, tuple)
        ), i.__class__.__name__
    assert sorted(v) == sorted(set(v)), repr(v)

    return shuffle_demon.choice(v)


def randint(*args):
    return random.randint(*args)


# - - - - non-randomness-related things


def capitalize(s):
    i = 0
    while i < len(s) and not s[i].isalpha():
        i += 1
    if i == 0:
        return s[0].upper() + s[1:]
    else:
        return s[:i] + s[i].upper() + s[i+1:]


def log(*args):
    sys.stderr.write(' '.join([str(a) for a in args]) + '\n')
