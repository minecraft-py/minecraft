import json

from server.utils import *


class Player():

    def __init__(self, uuid, name):
        self.uuid = uuid
        self.name = name
        self.strafe = [0, 0]
        self.position = (0, 0, 0)
        self.respawn_position = (0, 0, 0)
        self.rotation = (0, 0)

    def __str__(self):
        return 'Player(%s, %s)' % (self.uuid, self.name)

    def update_from_json(self, s):
        data = json.loads(s)
        self.strafe = data['strafe']

    def update(self, strafe, position, respawn_position, rotation):
        self.strafe = strafe
        self.position = position
        self.respawn_position = respawn_position
        self.rotation = rotation
