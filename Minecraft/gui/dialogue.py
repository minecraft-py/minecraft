import pyglet

import time

from Minecraft.utils.utils import *
from Minecraft.gui.base import GUI


class Dialogue(GUI):
    # 显示在左面的聊天记录

    def __init__(self):
        width, height = get_size()
        GUI.__init__(self, width, height)
        self.dialogue_label = pyglet.text.Label('',
                x=2, y=height - 75, width=width // 2, font_name='minecraftia', multiline=True)
        # 全部聊天内容
        self.dialogue = []
        # 实际显示的聊天内容
        self.shown = []
        # 最后一条聊天发送的时间
        self.last = time.time()

    def add_dialogue(self, text):
        self.dialogue.append(text)
        self.last = time.time()
        if len(self.shown) < 10:
            self.shown.append(text)
        else:
            self.shown.pop(0)
            self.shown.append(text)

    def draw(self):
        # 两个换行符表示真正的换行
        shown = ''
        for text in self.shown:
            shown += text + '\n'
        else:
            self.dialogue_label.text = shown
            self.dialogue_label.draw()
        
    def resize(self, width, height):
        self.dialogue_label.x = 2
        self.dialogue_label.y = height - 75
        self.dialogue_label.width = width // 2

    def update(self):
        if time.time() - self.last > 5.0:
            if len(self.dialogue) > 4096:
                self.dialogue.clear()
            if len(self.shown) > 0:
                self.shown.pop(0)
                self.last = time.time()
