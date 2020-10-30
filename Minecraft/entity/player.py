from Minecraft.entity.entity import Entity
from Minecraft.source import path
from Minecraft.utils.utils import *

from pyglet import graphics

class Player(Entity):

    def __init__(self):
        Entity.__init__(self)
        # 玩家模型
        self.batch = graphics.Batch()
        # 玩家的各个部分
        self.player = {}

    def draw(self):
        self.batch.draw()
