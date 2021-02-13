import math
import os
import time
import random

from Minecraft.source import path, settings
from Minecraft.utils.utils import *

import pyglet
from pyglet import image
from pyglet.gl import *
from pyglet.window import key, mouse


class Player():

    def __init__(self, game):
        self.game = game
        self._data = {}
        self._data['gamemode'] = 0
        self._data['block'] = 0
        self._data['stealing'] = False
        self._data['flying'] = False
        self._data['running'] = False
        self._data['die'] = False
        self._data['die_reason'] = ''
        self._data['in_hud'] = False
        self._data['in_chat'] = False
        self._data['hide_hud'] = False
        self._data['show_bag'] = False
        self._data['strafe'] = [0, 0]
        self._data['position'] = (0, 0, 0)
        self._data['respawn_position'] = (0, 0, 0)
        self._data['fov'] = settings['fov']
        self._data['rotation'] = (0, 0)
        self._data['dy'] = 0
        self._data['height'] = 2
        self._data['key_press'] = {}
        self._data['key_press']['w'] = {'count': 0, 'last': time.time()}
        self._data['key_press']['space'] = {'count': 0, 'last': time.time()}

    def __getitem__(self, item):
        return self._data.get(item, None)

    def __setitem__(self, item, value):
        if item in self._data:
            self._data[item] = value

    def collide(self, position):
        """
        碰撞检测

        :param: position, 玩家位置
        :return: position 碰撞检测之后的位置
        """
        pad = 0.25
        p = list(position)
        np = normalize(position)
        for face in FACES:
            for i in range(3):
                if not face[i]:
                    continue
                d = (p[i] - np[i]) * face[i]
                if d < pad:
                    continue
                for dy in range(self._data['height']):
                    op = list(np)
                    op[1] -= dy
                    op[i] += face[i]
                    if self.game.world.get(tuple(op)) is None:
                        continue
                    p[i] -= (d - pad) * face[i]
                    if face == (0, -1, 0) or face == (0, 1, 0):
                        self._data['dy'] = 0
                    break
        else:
            return tuple(p)

    def get_sight_vector(self):
        # 返回玩家的视线方向
        x, y = self._data['rotation']
        # y 的范围为 -90 到 90, 或 -pi/2 到 pi/2.
        # 所以 m 的范围为 0 到 1
        m = math.cos(math.radians(y))
        # dy 的范围为 -1 到 1. 玩家向下看为 -1, 向上看为 1
        dy = math.sin(math.radians(y))
        dx = math.cos(math.radians(x - 90)) * m
        dz = math.sin(math.radians(x - 90)) * m
        return (dx, dy, dz)

    def get_motion_vector(self):
        dy = dx = dz = 0.0
        x, y = self._data['rotation']
        strafe = math.degrees(math.atan2(*self._data['strafe']))
        y_angle = math.radians(y)
        x_angle = math.radians(x + strafe)
        if any(self._data['strafe']):
            if self._data['flying']:
                dx = math.cos(x_angle)
                dy = 0.0
                dz = math.sin(x_angle)
            else:
                dx = math.cos(x_angle)
                dy = 0.0
                dz = math.sin(x_angle)
        elif self._data['flying'] and not self._data['dy'] == 0:
            dx = 0.0
            dy = self._data['dy']
            dz = 0.0
        return (dx, dy, dz)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.game.exclusive and not self._data['die']:
            m = 0.1
            x, y = self._data['rotation']
            x, y = x + dx * m, y + dy * m
            if x >= 180:
                x = -180
            elif x<= -180:
                x = 180
            y = max(-90, min(90, y))
            self._data['rotation'] = (x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.game.exclusive:
            if self._data['gamemode'] == 1:
                return
            vector = self.get_sight_vector()
            now, previous = self.game.world.hit_test(self._data['position'], vector)
            if now:
                block = self.game.world.get(now)
            else:
                return
            if (button == mouse.RIGHT) or ((button == mouse.LEFT) and (modifiers & key.MOD_CTRL)) and now and previous:
                # 在 Mac OS X 中, Ctrl + 左键 = 右键
                if not self._data['die'] and not self._data['in_hud']:
                    if hasattr(block, 'on_use') and (not self._data['stealing']):
                        block.on_use(self)
                    elif previous and self.game.can_place(previous, self._data['position']):
                        self.game.world.add_block(previous, self.game.inventory[self._data['block']])
            elif button == pyglet.window.mouse.LEFT and previous:
                if block.hardness > 0 and not self._data['die'] and not self._data['in_hud']:
                    self.game.world.remove_block(now)
            elif button == pyglet.window.mouse.MIDDLE and block and previous:
                pass
        elif not self._data['die'] and not self._data['in_hud']:
            pass

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if self.game.exclusive:
            m = 0.1
            x, y = self._data['rotation']
            x, y = x + dx * m, y + dy * m
            if x >= 180:
                x = -180
            elif x<= -180:
                x = 180
            y = max(-90, min(90, y))
            self._data['rotation'] = (x, y)
            
            if self._data['gamemode'] == 1:
                return
            vector = self.get_sight_vector()
            now, previous = self.game.world.hit_test(self._data['position'], vector)
            if now:
                block = self.game.world.get(now)
            else:
                return
            if (button == mouse.RIGHT) or ((button == mouse.LEFT) and (modifiers & key.MOD_CTRL)) and now and previous:
                # 在 Mac OS X 中, Ctrl + 左键 = 右键
                if not self._data['die'] and not self._data['in_hud']:
                    if hasattr(block, 'on_use') and (not self._data['stealing']):
                        block.on_use(self)
                    elif previous and self.game.can_place(previous, self._data['position']):
                        self.game.world.add_block(previous, self.game.inventory[self._data['block']])
            elif button == pyglet.window.mouse.LEFT and previous:
                if block.hardness > 0 and not self._data['die'] and not self._data['in_hud']:
                    self.game.world.remove_block(now)
            elif button == pyglet.window.mouse.MIDDLE and block and previous:
                pass
        elif not self._data['die'] and not self._data['in_hud']:
            pass

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        scroll_y = -scroll_y
        index = int(self._data['block'] + scroll_y)
        if index > len(self.game.inventory) - 1:
            self._data['block'] = index = 0
        elif index < 0:
            self._data['block'] = index = len(self.game.inventory) - 1
        else:
            self._data['block'] = index
        self.game.hud['hotbar'].set_index(index)

    def on_key_press(self, symbol, modifiers):
        if self._data['in_chat']:
            if symbol == key.ESCAPE:
                self.game.menu['chat'].frame.enable(False)
                self.game.menu['chat'].text()
                self._data['in_chat'] = False
                self.game.set_exclusive_mouse(True)
            return
        if symbol == key.Q:
            self._data['die'] = True
            self._data['die_reason'] = 'killed by self'
            self.game.set_exclusive_mouse(False)
        elif symbol == key.T:
            if self.game.exclusive:
                self.game.set_exclusive_mouse(False)
                self._data['in_chat'] = not self._data['in_chat']
                self.game.menu['chat'].frame.enable()
        elif symbol == key.SLASH:
            if self.game.exclusive:
                self.game.set_exclusive_mouse(False)
                self._data['in_chat'] = not self._data['in_chat']
                self.game.menu['chat'].text('/')
                self.game.menu['chat'].frame.enable()
        elif symbol == key.W:
            if self._data['key_press']['w']['count'] == 1:
                if time.time() - self._data['key_press']['w']['last'] <= 0.1:
                    self._data['key_press']['w']['count'] = 2
                    self._data['running'] = True
                else:
                    self._data['key_press']['w']['count'] = 0
            self._data['key_press']['w']['last'] = time.time()
            self._data['strafe'][0] -= 1
        elif symbol == key.S:
            self._data['strafe'][0] += 1
        elif symbol == key.A:
            self._data['strafe'][1] -= 1
        elif symbol == key.D:
            self._data['strafe'][1] += 1
        elif symbol == key.I:
             if self.game.debug['enable']:
                self.game.debug['debug'] = not self.game.debug['debug']
                self.game.debug['position'] = False
        elif symbol == key.E:
            if not self._data['die']:
                self.game.set_exclusive_mouse(self._data['show_bag'])
                self._data['in_hud'] = not self._data['in_hud']
                self._data['show_bag'] = not self._data['show_bag']
        elif symbol == key.R:
            if self.game.debug['enable']:
                self.game.debug['running'] = not self.debug['running']
        elif symbol == key.K:
            for sector in self.game.world.sectors.values():
                print('sector:', sector)
                blocks = random.choices(sector, k=3)
                print('blocks:', blocks)
        elif symbol == key.SPACE:
            if self._data['key_press']['space']['count'] == 1:
                if time.time() - self._data['key_press']['space']['last'] <= 0.1:
                    self._data['key_press']['space']['count'] = 2
                    if self._data['gamemode'] != 1:
                        self._data['flying'] = not self._data['flying']
                else:
                    self._data['key_press']['space']['count'] = 0
            self._data['key_press']['space']['last'] = time.time()
            if self._data['flying']:
                self._data['dy'] = 0.1 * JUMP_SPEED
            elif self._data['dy'] == 0:
                self._data['dy'] = JUMP_SPEED
        elif symbol == key.ENTER:
            if self._data['die']:
                self._data['die'] = False
                self._data['position'] = self._data['respawn_position']
                self.game.set_exclusive_mouse(True)
        elif symbol == key.ESCAPE: 
                self.game.save(0)
                self.game.set_exclusive_mouse(False)
                self.game.menu['pause'].frame.enable()
                if self._data['die']:
                    self.game.close()
        elif symbol == key.LSHIFT:
            if self._data['flying']:
                self._data['dy'] = -0.1 * JUMP_SPEED
            else:
                self._data['stealing'] = True
        elif symbol in self.game.num_keys:
            self._data['block'] = (symbol - self.game.num_keys[0]) % len(self.game.inventory)
            self.game.hud['hotbar'].set_index(self._data['block'])
        elif symbol == key.F1:
            self._data['hide_hud'] = not self._data['hide_hud']
        elif symbol == key.F2:
            name = time.strftime('%Y-%m-%d_%H.%M.%S.png')
            pyglet.image.get_buffer_manager().get_color_buffer().save(os.path.join(
                path['screenshot'], name))
            self.game.dialogue.add_dialogue('Screenshot saved in: %s' % name)
        elif symbol == key.F3:
            self.game.debug['enable'] = True
        elif symbol == key.F11:
            self.game.set_fullscreen(not self.game.fullscreen)

    def on_key_release(self, symbol, modifiers):
        if self._data['in_chat']:
            return
        if symbol == key.W:
            if self._data['key_press']['w']['count'] == 0:
                self._data['key_press']['w']['count'] = 1
            elif self._data['key_press']['w']['count'] == 2:
                self._data['key_press']['w']['count'] = 0
                self._data['running'] = False
            self._data['key_press']['w']['last'] = time.time()
            self._data['strafe'][0] += 1
        elif symbol == key.S:
            self._data['strafe'][0] -= 1
        elif symbol == key.A:
            self._data['strafe'][1] += 1
        elif symbol == key.D:
            self._data['strafe'][1] -= 1
        elif symbol == key.SPACE:
            if self._data['key_press']['space']['count'] == 0:
                self._data['key_press']['space']['count'] = 1
            elif self._data['key_press']['space']['count'] == 2:
                self._data['key_press']['space']['count'] = 0
            self._data['key_press']['space']['last'] = time.time()
            if self._data['flying']:
                self._data['dy'] = 0
        elif symbol == key.LSHIFT:
            if self._data['flying']:
                self._data['dy'] = 0
            else:
                self._data['stealing'] = False
        elif symbol == key.F3:
            self.game.debug['enable'] = False
