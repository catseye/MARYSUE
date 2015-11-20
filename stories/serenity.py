from marysue.objects import (
    Object, Plural,
)
from marysue.characters import (
    MasculineCharacter, FeminineCharacter,
    MarySue, DreamBoat, Rival, TheOptimist,
    BadGuy, BadGal,
)
from marysue.settings import Setting


# - - - - settings - - - -


bridge = Setting(
    names=(
        'bridge of the Starship Dolphin',
        'bridge'
    ),
    roof=Object(names=('roof of the bridge',)),
    nearby=(
        Object(names=("Captain's chair",)),
        Object(names=('navigation dashboard',)),
        Object(names=("communications panel",)),
        Object(names=("air conditioning unit",)),
        Object(names=("view screen",)),
        Plural(names=("pulsing red and green lights",)),
        Object(names=("electro wrench",), takeable=True),
        Object(names=("cup of coffee",), takeable=True),
        Plural(names=("star charts",), takeable=True),
    ),
    has_drones=True,
    light='fluorescent light',
)

arch = Object(names=('crumbling arch',))

wasteland = Setting(
    names=(
        'rugged wastes of the planet Forbak',
        'wasteland',
        'blasted surface of Forbak',
    ),
    roof=arch,
    nearby=(
        Object(names=('gravel pit',)),
        arch,
        Object(names=('foundation of a ruined building',)),
        Plural(names=('sickly shrubs',)),
        Object(names=('oddly shaped rock',), takeable=True),
        Object(names=('dead snake',), takeable=True),
        Object(names=('vulture egg',), takeable=True),
    ),
    indoors=False,
    light='harsh sun light',
)

fortress = Setting(
    names=(
        "Nebulon's fortress stronghold",
        'stronghold fortress of Nebulon',
    ),
    roof=Object(names=('roof of the passage',)),
    nearby=(
        Plural(names=('manacles',)),
        Object(names=('door to the dungeon',)),
        Object(names=('torch in a thing on the wall',)),
        Object(names=('puddle of icky looking liquid',)),
        Plural(names=('bottle caps',), takeable=True),
        Plural(names=('shards of broken glass',), takeable=True),
        Object(names=('skull of a Space Rat',), takeable=True),
    ),
    preposition='in',
    outside_setting=wasteland,
    light='dim torch light',
)


settings = [bridge, wasteland, fortress]


# - - - - characters - - - -


serenity = MarySue(
    names=(
        "{rank} Serenity Starlight Warhammer O'James",
        "{rank} Serenity",
        "Serenity Starlight",
        "Serenity Starlight Warhammer O'James",
        "Ms. O'James",
    ),
    rank='Ensign',
    home=bridge,
    weapon=Object(names=(
        'Venusian Katana of Power',
    )),
)

joe = DreamBoat(
    names=(
        "{rank} Joe Mulbury",
        "Joe Mulbury",
        "{rank} Joe",
    ),
    home=bridge,
    rank='Commander',
    weapon=Object(names=('Jovian battle axe',)),
)

dwight = TheOptimist(
    names=(
        "{rank} Dwight Edgmont",
        "Dwight Edgmont",
        "{rank} Dwight",
    ),
    home=bridge,
    rank='Captain',
    weapon = Object(names=('vibro sword',)),
)

tammy = Rival(
    names=(
        "Navigator Tammy Smith",
        "Navigator Tammy",
        "Tammy Smith",
    ),
    home=bridge,
    rank='Lieutenant',
    weapon = Object(names=('electro mace',)),
)

protagonists = [serenity, joe, dwight, tammy]

nebulon = BadGuy(
    names=('Nebulon the Dastardly', 'Nebulon'),
    home=fortress
)

skull_witch = BadGal(
    names=('The Skull Witch',),
    home=fortress
)

antagonists = [nebulon, skull_witch]

power_staff = Object(names=('Venusian Staff of Power',))
eternity_jewel = Object(names=('Star Jewel of Eternity',))
hope_orb = Object(names=('Saturnian Orb of Hope',))
dream_chalice = Object(names=('Chalice of Dreams',))

macguffins = [power_staff, eternity_jewel, hope_orb, dream_chalice]

space_slugs = Plural(
    names=('Space Slugs',)
)
space_badgers = Plural(
    names=('Space Badgers',)
)
space_ferrets = Plural(
    names=('Space Ferrets',)
)
space_snails = Plural(
    names=('Space Snails',)
)
space_otters = Plural(
    names=('Space Otters',)
)
space_weasels = Plural(
    names=('Space Weasels',)
)
space_wallabies = Plural(
    names=('Space Wallabies',)
)
space_ostriches = Plural(
    names=('Space Ostriches',)
)

goons = [
    space_slugs, space_badgers, space_ferrets, space_snails,
    space_otters, space_weasels, space_wallabies, space_ostriches,
]
