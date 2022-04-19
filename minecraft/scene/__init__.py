from minecraft.utils.utils import *
from pyglet.event import EventDispatcher
from pyglet.window import Window


class Scene(EventDispatcher):

    def __init__(self, game):
        # 一个场景
        super().__init__()
    
    def on_scene_enter(self):
        # 场景特有的方法, 进入场景时调用
        pass

    def on_scene_leave(self):
        # 场景特有的方法, 离开场景时调用
        pass


class GameWindow(Window):

    def __init__(self, *args, **kwargs):
        # 游戏主窗口, 所有场景都绘制在这里
        super().__init__(*args, **kwargs)
        self.set_caption('Minecraft %s' % VERSION['str'])
        self._scenes = {}
        self._now = ''
    
    def add_scene(self, name, scene):
        # 添加场景
        self._scenes[name] = scene(self)
    
    def switch_scene(self, name):
        # 切换至一个场景
        if name not in self._scenes:
            pass
        if self._now != '':
            self.pop_handlers()
            self._scenes[self._now].on_scene_leave()
        self._now = name
        self.push_handlers(self._scenes[self._now])
        self._scenes[self._now].on_scene_enter()
