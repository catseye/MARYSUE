"""Settings for the story.

"""

import marysue.util as random
from marysue.objects import Object


class Setting(Object):
    def __init__(self, names, roof, nearby, indoors=True,
                       outside_setting=None,  # if given, this is another setting
                       preposition='on', has_drones=False,
                       light='light'):
        self.names = tuple(names)
        self._nearby = nearby
        self.roof = roof
        self.preposition = preposition
        self.has_drones = has_drones
        self.indoors = indoors
        self.outside_setting = outside_setting
        self.light = light
        assert all([isinstance(o, Object) for o in self._nearby])

    @property
    def nearby(self):
        return random.choice(self._nearby)

    @property
    def nearby_takeable(self):
        return random.choice(tuple(x for x in self._nearby if x.takeable))

    @property
    def nearby_scenery(self):
        return random.choice(tuple(x for x in self._nearby if not x.takeable))
