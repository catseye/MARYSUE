# encoding: UTF-8

"""Abstract Story Trees.

"""

import re

import marysue.util as random


ALIASES = {
    'indef': 'indefinite',
    'def': 'definite',
    'obj': 'object',
    'sub': 'subject',
    'subj': 'subject',
    'his': 'possessive_pronoun',
    'her': 'possessive_pronoun',
    'he': 'pronoun',
    'she': 'pronoun',
}


class AST(object):
    slots = None
    templates = None

    def __init__(self, *args, **kwargs):
        self._children = args
        if self.slots is not None:
            for key, value in kwargs.iteritems():
                if key not in self.slots:
                    raise AttributeError(
                        "{0} has no attribute '{1}'".format(
                            self.__class__.__name__, key
                        )
                    )
            for key in self.slots:
                kwargs.setdefault(key, None)
        self._attrs = kwargs

    def __repr__(self):
        children = ', '.join([repr(c) for c in self._children])
        attrs = ', '.join(['%s=%r' % (key, value) for key, value in self._attrs.iteritems() if value is not None])
        j = ', ' if children and attrs else ''
        return "%s(%s%s%s)" % (self.__class__.__name__, children, j, attrs)

    def repr_abbrev(self):
        attrs = ', '.join(['%s=%r' % (key, value) for key, value in self._attrs.iteritems() if value is not None])
        return "%s(%s)" % (self.__class__.__name__, attrs)

    def dump(self, f, indent=0):
        f.write(' ' * indent)
        f.write(self.repr_abbrev())
        f.write('\n')
        for child in self:
            child.dump(f, indent + 2)

    def __getitem__(self, index):
        return self._children[index]

    def __iter__(self):
        return self._children.__iter__()

    def __getattr__(self, name):
        if name in self._attrs:
            return self._attrs[name]
        raise AttributeError(name)

    def iteritems(self):
        return self._attrs.iteritems()

    def flatten(self):
        """Individual nodes which you want to flatten must define how they are to be flattened"""
        return self.__class__(*[c.flatten() for c in self], **dict(self.iteritems()))

    def insert(self, position, *args, **kwargs):
        """Returns a new AST node"""
        children = [c for c in self]
        for a in args:
            children.insert(position, a)
            position += 1
        attrs = dict((k, v) for k, v in self.iteritems())
        attrs.update(kwargs)
        return self.__class__(*children, **attrs)

    def render_t_impl(self, template):

        def pick_one(match):
            return random.choice(tuple(match.group(1).split('|')))
        template = re.sub(r'\<(.*?)\>', pick_one, template)

        def repl(match):
            parts = [ALIASES.get(part, part) for part in match.group(1).split('.') if part]
            try:
                obj = self._attrs[parts.pop(0)]
            except KeyError:
                print self
                raise
            while parts:
                obj = getattr(obj, parts.pop(0))
            return obj
        return re.sub(r'\{([a-zA-Z0-9_.]+)\}', repl, template)

    def render_t(self, template):
        try:
            return self.render_t_impl(template)
        except Exception:
            print
            print "!!! error in template '%s' on ast %r" % (template, self)
            print
            raise

    def render(self):
        if self.templates:
            # TODO why is random.choice() not sufficient here?
            template = random.shuffle_demon.choice(self.templates)
            return self.render_t(template)
        raise NotImplementedError(repr(self))

    def __unicode__(self):
        return self.render()


# TODO AST should inherit from this

class Properties(object):
    """Please treat as immutable"""

    slots = None

    def __init__(self, **kwargs):
        if self.slots is not None:
            for key, value in kwargs.iteritems():
                if key not in self.slots:
                    raise AttributeError(
                        "{0} has no attribute '{1}'".format(
                            self.__class__.__name__, key
                        )
                    )
            for key in self.slots:
                kwargs.setdefault(key, None)
        self._attrs = kwargs

    def __repr__(self):
        attrs = ', '.join(['%s=%r' % (key, value) for key, value in self._attrs.iteritems() if value is not None])
        return "%s(%s)" % (self.__class__.__name__, attrs)

    def __getattr__(self, name):
        if name in self._attrs:
            return self._attrs[name]
        raise AttributeError(name)

    def __setattr__(self, name, value):
        if name not in ('_attrs',):
            raise AttributeError(name)
        return super(Properties, self).__setattr__(name, value)

    def iteritems(self):
        return self._attrs.iteritems()

    def clone(self, **kwargs):
        attrs = self._attrs.copy()
        attrs.update(kwargs)
        return self.__class__(**attrs)
