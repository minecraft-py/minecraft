from Minecraft.source import settings

from pyglet import graphics


class Player():

    def __init__(self):
        self._element = {}
        self._element['stealing'] = False
        self._element['can_fly'] = False
        self._element['flying'] = False
        self._element['running'] = False
        self._element['die'] =  False
        self._element['die_reason'] = ''
        self._element['in_hud'] = False
        self._element['hide_hud'] = False
        self._element['show_bag'] = False
        self._element['strafe'] = [0, 0]
        self._element['rotate'] = (0, 0)
        self._element['position'] = (0, 0, 0)
        self._element['respawn_position'] = (0, 0, 0)
        self._element['fov'] = settings['fov']
        self.camera = Camera(self._element['position'])
        self.camera.rotate(*self._element['rotate'])

    def look(self):
        self.camera.goto(self._element['position'])
        self.camera.transform()
        self.camera.look()

    def get(self, name):
        if name in self._element:
            return self._element['name']
        else:
            return

    def set(self, name, value):
        if name in self._element:
            self._element[name] = value


class PlayerGroup():

    def __init__(self):
        # 能够控制的玩家
        self.player = Player()
        # 其余的玩家
        self.group = {}
