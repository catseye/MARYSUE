import marysue.util as random
from marysue.objects import Object, Plural, MasculineMixin, FeminineMixin


# since the first argument is always a Character, arguably, these
# functions should all be methods on Character instead.  Oh well.


def make_costume(character, item_choices):
    adjective = character.costume_adjective
    if adjective:
        adjective = adjective + ' '
    colour = character.colour
    material = random.choice(character.costume_materials)
    (item, cls_) = random.choice(item_choices)
    with_ = character.costume_decoration

    names = (
        '{}{} {} {}{}'.format(adjective, colour, material, item, with_),
        item
    )

    return cls_(names=names)


def make_torso_costume(character):
    item_choices = (
        'jacket', 'shirt', 'jerkin', 'top', 'jersey', 'suit jacket',
        'sweater', 'hoodie', 'jumper',
    )

    if isinstance(character, FeminineMixin):
        item_choices += ('blouse', 'halter top', 'tank top', 'frock',)

    if isinstance(character, MasculineMixin):
        item_choices += ('muscle shirt',)

    return make_costume(character, tuple((item, Object) for item in item_choices))


def make_legs_costume(character):
    item_choices = tuple((item, Plural) for item in (
        'trousers', 'leggings', 'slacks', 'culottes',
        # 'hose',
    ))

    if isinstance(character, FeminineMixin):
        item_choices += (('skirt', Object),)

    return make_costume(character, item_choices)


def make_onesie_costume(character):
    item_choices = tuple((item, Object) for item in (
        'jumpsuit', 'track suit', 'robe', 'smock',
        'long coat', 'trench coat', 'great coat',
    )) + (('coveralls', Plural),)

    if isinstance(character, FeminineMixin):
        item_choices += tuple((item, Object) for item in (
            'dress', 'gown', 'leotard',
        ))

    return make_costume(character, item_choices)


def make_feet_costume(character):
    item_choices = tuple((item, Plural) for item in (
        'boots', 'shoes', 'sandals', 'sneakers', 'trainers',
        'dress shoes'
    ))

    if isinstance(character, FeminineMixin):
        item_choices += (('pixie boots', Plural), ('pumps', Plural))

    return make_costume(character, item_choices)
