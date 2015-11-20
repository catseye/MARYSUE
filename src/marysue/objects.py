"""Objects in the story.

This includes characters, which are merely animate objects.  And settings.

The root object of all objects is Object.

Objects here contain only the properties of the object which do not change during the
course of the story.  See marysue.state.State for states of objects over time.

"""

import string

import marysue.util as random


class Object(object):
    """Objects are immutable."""

    def __init__(self, names, takeable=False, home=None, rank=None, weapon=None):
        self.names = tuple(names)
        self.takeable = takeable
        self.home = home
        self.rank = rank
        self.weapon = weapon

    def __hash__(self):
        return hash(self.names)
        # ...and the other stuff too, I guess, but in practice no.

    def __eq__(self, other):
        return isinstance(other, Object) and self.names == other.names
        # ...and the other stuff too, I guess, but in practice no.

    def __repr__(self):
        return "%s(names=%r)" % (self.__class__.__name__, self.names)
        # ...and the other stuff too, I guess, but in practice no.

    @property
    def name(self):
        return self.names[0].replace('{rank}', str(getattr(self, 'rank', '')))

    @property
    def indefinite_article(self):
        return 'a '

    @property
    def definite_article(self):
        return 'the '

    # Not sure how I feel about these three methods -- see marysue.state.State

    @property
    def definite(self):
        article = self.definite_article
        fnite = self._fnite()
        return article + fnite

    @property
    def indefinite(self):
        article = self.indefinite_article
        fnite = self._fnite()
        if article == 'a 'and fnite[0].upper() in ('A', 'E', 'I', 'O', 'U'):
            article = 'an '
        return article + fnite

    def _fnite(self):
        return self.name

    @property
    def possessive(self):
        return self.definite + "'s"

    @property
    def possessive_pronoun(self):
        return 'its'

    @property
    def accusative_pronoun(self):
        return "it"

    @property
    def accusative(self):
        return self.accusative_pronoun

    @property
    def pronoun(self):
        return "it"

    @property
    def distal_pronoun(self):
        return 'that'

    @property
    def proximal_pronoun(self):
        return 'this'

    @property
    def distal(self):
        return self.distal_pronoun + " " + self._fnite()

    @property
    def proximal(self):
        return self.proximal_pronoun + " " + self._fnite()

    @property
    def was(self):
        return "was"

    @property
    def colours(self):
        return (
            'red', 'yellow', 'blue', 'purple', 'green', 'orange',
            'mauve', 'brown', 'black', 'white',
            'tan', 'chartreuse', 'maroon', 'pink', 'violet',
            'orange red', 'blue green', 'navy blue',
            'gold coloured', 'silver coloured',
            #'fuschia', 'ecru', 'puce',

            'floral print', 'plaid', 'tie dyed', 'pinstripe',
            # 'herringbone', 
            # 'houndstooth',
        )

    @property
    def colour(self):
        return random.choice(self.colours)

    @property
    def gibberish(self):
        def w():
            return ''.join(random.lowercase() for _ in xrange(0, random.randint(3, 8)))
        words = [w() for _ in xrange(0, random.randint(3, 9))]
        return ' '.join(words)


class PluralMixin(object):
    @property
    def indefinite_article(self):
        return 'some '

    @property
    def definite_article(self):
        return 'the '

    @property
    def possessive_pronoun(self):
        return "their"

    @property
    def accusative_pronoun(self):
        return "them"

    @property
    def pronoun(self):
        return "them"

    @property
    def distal_pronoun(self):
        return 'those'

    @property
    def proximal_pronoun(self):
        return 'these'

    @property
    def was(self):
        return "were"

    @property
    def singular(self):
        if self.name.endswith('s'):
            return self.name[:-1]
        else:
            return self.name


class Plural(PluralMixin, Object):
    pass


class ProperMixin(object):
    @property
    def indefinite_article(self):
        return ''

    @property
    def definite_article(self):
        return ''


class Proper(ProperMixin, Object):
    pass


class MasculineMixin(ProperMixin):
    @property
    def possessive_pronoun(self):
        return "his"

    @property
    def accusative_pronoun(self):
        return "him"

    @property
    def pronoun(self):
        return "he"


class FeminineMixin(Object):
    @property
    def possessive_pronoun(self):
        return "her"

    @property
    def accusative_pronoun(self):
        return "her"

    @property
    def pronoun(self):
        return "she"


class Group(PluralMixin):
    def __init__(self, *subjects):
        if len(subjects) == 0:
            raise ValueError("Group must include at least one object")
        self.subjects = subjects

    def __repr__(self):
        children = ', '.join([repr(c) for c in self.subjects])
        return "%s(%s)" % (self.__class__.__name__, children)

    def __iter__(self):
        return self.subjects.__iter__()

    def __getitem__(self, index):
        return self.subjects[index]

    def __len__(self):
        return len(self.subjects)

    def __add__(self, other):
        total = self.subjects + tuple(o for o in other)
        return Group(*total)

    @property
    def definite(self):
        if len(self.subjects) == 0:
            return 'no one'
        elif len(self.subjects) == 1:
            return self.subjects[0].definite
        elif len(self.subjects) == 2:
            return self.subjects[0].definite + ' and ' + self.subjects[1].definite
        return ', '.join([s.definite for s in self.subjects[:-1]]) + ', and ' + self.subjects[-1].definite

    @property
    def pronoun(self):
        return self.definite
