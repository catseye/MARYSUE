import marysue.util as random
from marysue.ast import Properties
from marysue.objects import Object
from marysue.duties import Duty


class State(Properties):
    """State of a character (or other object) at a given point in the story.

    Each State references an Object, which contains the properties of
    that story-object that do not change over the course of the story.

    AST nodes should generally reference a State instead of an Object.
    We have a pass which replaces Objects in ASTs with the State of that
    Object at that particular time (depth-first, i.e. leftmost innermost
    traversal, mapping to time.)  Further passes read and update that
    State on each instantaneous appearance on each Object.

    """
    slots = ('object',
             'is_referent',
             'first_occurrence',
             'torso_costume',
             'legs_costume',
             'feet_costume',
             'hands_costume',
             'head_costume',
             'duties',
             'mood',
             'location',)

    def __init__(self, object, **kwargs):
        assert isinstance(object, Object), repr(object)
        kwargs['object'] = object
        super(State, self).__init__(**kwargs)

    def __getattr__(self, name):
        if name in self.slots:
            return self._attrs[name]
        if not hasattr(self.object, name) and name not in dir(self.object):
            # FIXME should be AttributeError but something catches that
            raise KeyError(name)
        return getattr(self.object, name)

    # Not sure how I feel about these three methods, but, OK
    # (Because State just delegates to Object, and Object doesn't know to do this from inside itself)

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
        # helper function
        if not self.first_occurrence:
            if len(self.object.names) == 1:
                return self.object.name
            else:
                r = random.choice(self.object.names[1:])
                return r.replace('{rank}', str(getattr(self.object, 'rank', '')))
        else:
            return self.object.name

    @property
    def pronoun(self):
        if self.is_referent:
            return self.object.pronoun
        else:
            return self.definite

    @property
    def accusative(self):
        if self.is_referent:
            return self.object.accusative
        else:
            return self.definite

    @property
    def possessive(self):
        if self.is_referent:
            return self.object.possessive_pronoun
        else:
            return self.object.possessive

    @property
    def adverb(self):
        assert self.mood, 'mood not assigned to %r' % self
        adverbs = {
            'happy': (
                'courageously', 'obsequiously', 'fawningly', 'blissfully',
                'virtuously', 'happily', 'lightly', 'energetically',
                'laughingly', 'placidly', 'peacefully', 'calmly',
                'enigmatically',
                'strongly', 'firmly',
            ),
            'sad': (
                'drily', 'heavily', 'irritatedly', 'exasperatedly',
                'slowly', 'drably', 'unhappily', 'sadly', 'irksomely',
                'weakly', 'downheartedly', 'grumpily',
                'enigmatically',
            ),
            'angry': (
                'viciously', 'menacingly', 'drily', 'gratingly', 'heavily',
                'threateningly', 'firmly', 'impatiently',
                'icily', 'acidly', 'sternly',
                'emphatically', 'annoyingly', 'irritatedly', 'exasperatedly',
                'outrageously', 'strongly',
                'enigmatically',
                # 'cunningly', 'slyly',
            ),
            'embarrassed': (
                'awkwardly', 'slumblingly', 'coyly', 'slowly',
                'carefully', 'painfully', 'painingly',
                'enigmatically',
                # 'cunningly', 'slyly',
            ),
        }
        return random.choice(adverbs[self.mood])

    @property
    def saids(self):
        return {
            'happy': (
                'said', 'stated', 'chirped', 'smiled',
                'sighed', 'breathed', 'whispered', 'giggled',
                'drawled',
            ),
            'sad': (
                'said', 'groaned', 'muttered', 'intoned', 'droned',
                'gasped', 'gulped', 'mumbled', 'bleated',
            ),
            'angry': (
                'said', 'groaned', 'muttered',
                'intoned', 'barked', 'splurted',
                'bellowed', 'shouted', 'yelled', 'raged',
            ),
            'embarrassed': (
                'said', 'groaned', 'muttered',
                'whispered', 'mumbled',
                'gasped', 'gulped', 'sighed', 'breathed',
            ),
        }

    @property
    def said(self):
        assert self.mood, 'mood not assigned to %r' % self
        return random.choice(self.saids[self.mood])

    @property
    def shouteds(self):
        return {
            'happy': (
                'exclaimed', 'yelled', 'squealed', 'yelped', 'shouted',
                'cried',
            ),
            'sad': (
                'exclaimed', 'yelped', 'shouted',
                'gasped', 'gulped', 'screeched', 'cried',
            ),
            'angry': (
                'yelled', 'screeched', 'shouted',
                'screamed', 'bellowed', 'barked',
            ),
            'embarrassed': (
                'yelled', 'yelped', 'screamed', 'shouted',
                'gasped', 'gulped', 'screeched', 'cried',
            ),
        }

    @property
    def shouted(self):
        assert self.mood, 'mood not assigned to %r' % self
        return random.choice(self.shouteds[self.mood])

    @property
    def emoted(self):
        assert self.mood, 'mood not assigned to %r' % self
        emoteds = {
            'happy': (
                'smiled', 'whistled', 'grinned', 'beamed', 'winked',
            ),
            'sad': (
                'frowned', 'gasped', 'blinked', 'pouted',
            ),
            'angry': (
                'frowned', 'grimaced', 'blinked',
            ),
            'embarrassed': (
                'blushed', 'frowned', 'looked away',
            ),
        }
        return random.choice(emoteds[self.mood])

    @property
    def pick_duty(self):
        if self.duties:
            return random.choice(self.duties)
        else:
            return Duty(names=('uphold the code of the Star Fighters',))
