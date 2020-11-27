import json

from server.utils import *


class Player():

    def __init__(self, uuid):
        self.uuid = uuid
        self.player = {}
        self.player['position'] = (0, 0, 0)

    def __str__(self):
        return 'Player(%s, %s)' % (self.uuid)

    def get_json(self):
        data = {
                'position': pos2str(self.player['position'])
            }
        return 'player {0} {1}'.format(self.uuid, json.dumps(data))
    
    def update_from_json(self, s):
        data = json.loads(s)
        self.strafe = str2pos(data['position'], True)

    def update(self, position):
        self.position = position
