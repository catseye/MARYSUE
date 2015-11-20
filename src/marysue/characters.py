import marysue.util as random
from marysue.objects import Proper, MasculineMixin, FeminineMixin, Group


# - - - - ranks - - - -

RANKS = (
    'Ensign',
    'Lieutenant',
    'Lieutenant Commander',
    'Commander',
    'Captain',
    'Commodore',
    'Admiral',
    'Super Admiral',
)


class Character(Proper):
    def __init__(self, names, **kwargs):
        super(Character, self).__init__(names, **kwargs)
        self.stature = random.choice((
            'somewhat short',
            'of average height',
            'rather tall',
        ))
        self.hair_length = random.choice((
            'long',
            'shoulder length',
            'short',
            'close cropped',
        ))
        self.hair_colour = random.choice((
            'blonde', 'brown', 'red', 'auburn', 'black',
        ))
        self.eye_colour = random.choice((
            'brown', 'blue', 'grey', 'green', 'hazel',
        ))
        self.war_cry = "BY THE " + random.choice((
            'MOONS',
            'RINGS',
            'MOUNTAINS',
            'METEORS',
        )) + " OF " + random.choice((
            'VENUS',
            'MARS',
            'JUPITER',
            'NEPTUNE',
        ))

    @classmethod
    def characters_to_set(cls, *args):
        """Not the most intuitive place for this method?  Oh well."""
        s = set()
        for arg in args:
            if arg is None:
                continue
            if isinstance(arg, Group):
                for c in arg:
                    s.add(c)
            else:
                s.add(arg)
        return set([p for p in s if isinstance(p, cls)])

    def promote(self):
        """Mutates this character.  One of the few methods that'll do that."""
        self.rank = self.next_rank

    @property
    def next_rank(self):
        for n, r in enumerate(RANKS):
            if r == self.rank:
                return RANKS[n + 1]

    @property
    def costume_materials(self):
        return (
            'silk', 'leather',
            'polyester', 'cotton', 'nylon', 'denim',
            'rayon', 'dacron', 'crinkly foil',
            #  'woolen' is far too weird for most things, esp. footwear
            #  'suede' is likewise a little weird
        )

    @property
    def costume_decorations(self):
        return (
            ' with {colour} stripes',
            ' with {colour} {costume_material} trim',
        )

    @property
    def costume_decoration(self):
        if random.chance(75):
            return ''
        return random.choice(self.costume_decorations).format(
            colour=self.colour,
            costume_material=random.choice(self.costume_materials),
        )

    @property
    def costume_adjectives(self):
        return (
            'fine',
            'snappy',
            'handsome',
        )

    @property
    def costume_adjective(self):
        if random.chance(60):
            return ''
        else:
            return random.choice(self.costume_adjectives)

    @property
    def wearing(self):
        return random.choice((
            'wearing', 'sporting', 'looking fine in',
            'looking smashing in', 'looking delightful in',
            'looking impressive in', 'decked out in'
        ))

    @property
    def yet(self):
        return '{} yet {}'.format(
            random.choice((
                'smooth', 'graceful', 'gentle', 'supple', 'soft', 'exquisite',
            )),
            random.choice((
                'powerful', 'forceful', 'firm', 'masterful', 'confident', 'strong',
            ))
        )

    @property
    def motion(self):
        if random.chance(80):
            return ''
        return 'with a {} motion, '.format(self.yet)

    @property
    def simile(self):
        return 'like {} {}'.format(
            random.choice((
                'a tiger',
                'charcoal',
                'an elephant',
                'a ninja',
                'a gangster',
                'a giraffe',
                'a hurricane',
                'a samurai',
                'a rabid dog',
                'a crazed bull',
                'a baboon',
                'a gorilla',
            )),
            random.choice((
                'in a snowstorm',
                'in a rainstorm',
                'piloting a helicopter',
                'driving a race car',
                'in a gymnasium parking lot',
                'in a pet shop',
                'in a bazaar',
                'in a video arcade',
                'at a baseball game',
                'in a performance art piece',
                'in a jewellery store',
                'in a mosh pit',
                'at a square dance',
                'at a monster truck rally',
            ))
        )

    @property
    def withvoice(self):
        return 'with a voice ' + self.simile


class MasculineCharacter(MasculineMixin, Character):
    def __init__(self, names, **kwargs):
        super(MasculineCharacter, self).__init__(names, **kwargs)
        self.feature_adj = random.choice((
            'strong', 'deep', 'wide', 'large',
        ))
        self.feature = random.choice((
            'nose', 'mouth', 'brow', 'chin',
        ))


class FeminineCharacter(FeminineMixin, Character):
    def __init__(self, names, **kwargs):
        super(FeminineCharacter, self).__init__(names, **kwargs)
        self.feature_adj = random.choice((
            'small', 'perky', 'narrow', 'large',
        ))
        self.feature = random.choice((
            'nose', 'mouth', 'forehead', 'chin',
        ))


class MarySue(FeminineCharacter):
    def __init__(self, names, **kwargs):
        super(MarySue, self).__init__(names, **kwargs)
        self.feature_adj = random.choice((
            'wicked cute', 'perfect', 'beautiful', 'enchanting',
        ))
        self.feature = random.choice((
            'nose', 'mouth', 'forehead', 'chin',
        ))
        self.stature = random.choice((
            'enchantingly petite',
            'a bit on the short side, but in a cute way',
            'neither short nor tall but not average either',
            'sort of tall for a girl, but not in a bad way',
        ))
        self.hair_length = random.choice((
            'exceptionally long (down to her knees)',
            'wicked long (down to her knees)',
            'beautiful long',
            'perky shoulder length',
        ))
        self.hair_colour = random.choice((
            'purple', 'indigo', 'violet', 'midnight black',
            'black and purple',
            'multi coloured', 'rainbow coloured', 'multi hued',
            'rainbow hued', 'shimmering rainbow coloured',
            'shimmering multi hued', 'shimmering rainbow hued',
        ))
        self.eye_colour = random.choice((
            'purple', 'indigo', 'violet', 'icy blue',
            'multi coloured', 'rainbow coloured', 'multi hued', 'rainbow hued',
            'shimmering multi coloured', 'shimmering rainbow coloured', 'shimmering multi hued', 'shimmering rainbow hued',
            'kaleidoscope coloured', 'shimmering kaleidoscope coloured',
        ))

    @property
    def colours(self):
        return (
            'purple', 'dark purple', 'pale purple',
            'violet', 'dark violet', 'pale violet',
            'indigo', 'dark indigo', 'pale indigo',
            'red and purple', 'purple and gold', 'black and purple',
            'crimson', 'crimson and purple', 'crimson and violet',
            'purple and white', 'purple and violet', 'blue and purple',
            'midnight black', 'white',

            'multi coloured', 'rainbow coloured', 'multi hued',
            'rainbow hued', 'shimmering rainbow coloured',
            'shimmering multi hued', 'shimmering rainbow hued',

            'gold coloured', 'silver coloured', 'silvery',
            'silver and purple', 'shiny silver', 'shiny purple',
            'deep violet', 'deep indigo', 'shimmering purple',
        )

    @property
    def costume_decorations(self):
        return (
            ' with frilly {colour} lace',
            ' with {colour} lacy frills',
            ' with {colour} lightning bolt patterns',
            ' with {colour} star patterns',
            ' with {colour} moon beam patterns',
            ' adorned with {gems}',
            ' with {colour} {costume_material} trim',
        )

    @property
    def costume_decoration(self):
        return random.choice(self.costume_decorations).format(
            colour=self.colour,
            costume_material=random.choice(self.costume_materials),
            gems=random.choice((
                'jewels', 'gems', 'rubies', 'emeralds', 'sapphires',
            )),
        )

    @property
    def costume_adjectives(self):
        return (
            '',
            'beautiful',
            'elegant',
            'exquisite',
            'fantastic',
            'marvellous',
        )

    @property
    def costume_adjective(self):
        if random.chance(4):
            return 'WICKED AWESOME'
        else:
            return random.choice(self.costume_adjectives)


class DreamBoat(MasculineCharacter):
    def __init__(self, names, **kwargs):
        super(DreamBoat, self).__init__(names, **kwargs)
        self.feature_adj = random.choice((
            'handsome', 'perfect', 'beautiful', 'enthralling',
        ))
        self.feature = random.choice((
            'nose', 'mouth', 'brow', 'chin',
        ))
        self.stature = random.choice((
            'a bit on the short side, but in a cute way',
            'of perfectly normal height like a normal person should be',
            'quite tall, but really handsomely tall, not freakishly tall',
        ))


class Rival(FeminineCharacter):
    @property
    def wearing(self):
        return random.choice((
            'wearing', 'looking frumpy in',
            'looking tastless in', 'looking completely unimpressive in',
            'gotten up in',
        ))

    @property
    def costume_decorations(self):
        return (
            ' with gaudy {colour} polka dots',
            ' with a tacky {colour} zig zag pattern',
        )

    @property
    def costume_adjectives(self):
        return (
            '',
            'ill fitting',
            'tacky',
            'tasteless',
            'gaudy',
            'bleak',
            'outdated',
        )


class TheOptimist(MasculineCharacter):
    @property
    def wearing(self):
        return random.choice((
            'wearing', 'sporting', 'looking exciting in',
            'resplendent in', 'looking ready for action in',
        ))


class BaddieMixin(object):
    @property
    def wearing(self):
        return random.choice((
            'wearing', 'looking menacing in',
            'looking villanous in', 'looking impressive in',
            'gotten up in', 'looking intimidating in',
        ))

    @property
    def colours(self):
        return (
            'black', 'midnight black', 'dark black', 'deep black',
            'red', 'dark red', 'blood red', 'blood coloured', 'deep red',
        )


class BadGuy(BaddieMixin, MasculineCharacter):
    def __init__(self, names, **kwargs):
        super(BadGuy, self).__init__(names, **kwargs)
        self.feature_adj = random.choice((
            'ugly', 'jutting', 'overbearing', 'scarred',
        ))
        self.feature = random.choice((
            'nose', 'mouth', 'brow', 'chin',
        ))
        self.hair_colour = random.choice((
            'black', 'platinum blonde', 'white', 'green',
        ))


class BadGal(BaddieMixin, FeminineCharacter):
    def __init__(self, names, **kwargs):
        super(BadGal, self).__init__(names, **kwargs)
        self.feature_adj = random.choice((
            'ugly', 'jutting', 'overbearing', 'scarred',
        ))
        self.feature = random.choice((
            'nose', 'mouth', 'brow', 'chin',
        ))
        self.hair_colour = random.choice((
            'black', 'platinum blonde', 'white', 'green',
        ))
