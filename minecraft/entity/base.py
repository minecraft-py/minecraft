import uuid

from minecraft.utils.nbt import NBT


class Entity():

    def __init__(self, position, rotation=(0, 0), health=0, max_health=0, nbt=None):
        self._data = dict()
        self._data['position'] = position
        self._data['rotation'] = rotation
        self._data['health'] = health
        self._data['alive'] = 0
        self.max_health = max_health
        self.entity_id = str(uuid.uuid4())
        if nbt is not None:
            self.from_nbt(nbt)

    def from_nbt(self, nbt):
        for k, v in nbt.get_dict().items():
            self._data[k] = v
        else:
            self._data['position'] = tuple(self._data['position'])
            self._data['rotation'] = tuple(self._data['rotation'])

    def get_data(self):
        self._data['alive'] = round(self._data['alive'], 3)
        return self._data

    def on_update(self, dt):
        self._data['alive'] += dt

    def on_draw(self):
        pass
