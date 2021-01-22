import os
import time

from Minecraft.source import settings
from Minecraft.utils.utils import *

import pyglet
from pyglet import image
from pyglet.gl import *
from pyglet.window import key, mouse


class Player():

    def __init__(self):
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

    def __getitem__(self, item):
        return self._data.get(item, None)

    def __setitem__(self, item, value):
        if item in self._data:
            self._data[item] = value

    def on_mouse_motion(self, x, y, dx, dy):
        if get_game().exclusive and not self._data['die']:
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
        if get_game().exclusive:
            if self._data['gamemode'] == 1:
                return
            vector = get_game().get_sight_vector()
            now, previous = get_game().world.hit_test(self._data['position'], vector)
            if now:
                block = get_game().world.get(now)
            else:
                return
            if (button == mouse.RIGHT) or ((button == mouse.LEFT) and (modifiers & key.MOD_CTRL)) and now and previous:
                # 在 Mac OS X 中, Ctrl + 左键 = 右键
                if not self._data['die'] and not self._data['in_hud']:
                    if hasattr(block, 'on_use') and (not self._data['stealing']):
                        block.on_use(self)
                    elif previous and get_game().can_place(previous, self._data['position']):
                        get_game().world.add_block(previous, get_game().inventory[self._data['block']])
            elif button == pyglet.window.mouse.LEFT and previous:
                if block.hardness > 0 and not self._data['die'] and not self._data['in_hud']:
                    get_game().world.remove_block(now)
            elif button == pyglet.window.mouse.MIDDLE and block and previous:
                pass
        elif not self._data['die'] and not self._data['in_hud']:
            pass

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        index = int(self._data['block'] + scroll_y)
        if index > len(get_game().inventory) - 1:
            self._data['block'] = index = 0
        elif index < 0:
            self._data['block'] = index = len(get_game().inventory) - 1
        else:
            self._data['block'] = index
        get_game().hud['hotbar'].set_index(index)

    def on_key_press(self, symbol, modifiers):
        if self._data['in_chat']:
            if symbol == key.ESCAPE:
                get_game().menu['chat'].frame.enable(False)
                get_game().menu['chat'].text()
                self._data['in_chat'] = False
                get_game().set_exclusive_mouse(True)
            return
        if symbol == key.Q:
            self._data['die'] = True
            self._data['die_reason'] = 'killed by self'
            get_game().set_exclusive_mouse(False)
        elif symbol == key.T:
            if get_game().exclusive:
                get_game().set_exclusive_mouse(False)
                self._data['in_chat'] = not self._data['in_chat']
                get_game().menu['chat'].frame.enable()
        elif symbol == key.SLASH:
            if get_game().exclusive:
                get_game().set_exclusive_mouse(False)
                self._data['in_chat'] = not self._data['in_chat']
                get_game().menu['chat'].text('/')
                get_game().menu['chat'].frame.enable()
        elif symbol == key.W:
            self._data['strafe'][0] -= 1
        elif symbol == key.S:
            self._data['strafe'][0] += 1
        elif symbol == key.A:
            self._data['strafe'][1] -= 1
        elif symbol == key.D:
            self._data['strafe'][1] += 1
        elif symbol == key.I:
             if not get_game().ext['enable']:
                get_game().ext['debug'] = not get_game().ext['debug']
                get_game().ext['position'] = False
        elif symbol == key.E:
            if not self._data['die']:
                get_game().set_exclusive_mouse(self._data['show_bag'])
                self._data['in_hud'] = not self._data['in_hud']
                self._data['show_bag'] = not self._data['show_bag']
        elif symbol == key.P:
            if get_game().ext['enable']:
                get_game().ext['position'] = not self.ext['position']
                get_game().ext['debug'] = False
        elif symbol == key.R:
            if get_game().ext['enable']:
                get_game().ext['running'] = not self.ext['running']
        elif symbol == key.SPACE:
            if self._data['flying']:
                self._data['dy'] = 0.1 * JUMP_SPEED
            elif self._data['dy'] == 0:
                self._data['dy'] = JUMP_SPEED
        elif symbol == key.ENTER:
            if self._data['die']:
                self._data['die'] = False
                self._data['position'] = self._data['respawn_position']
                get_game().set_exclusive_mouse(True)
        elif symbol == key.ESCAPE: 
                get_game().save(0)
                get_game().set_exclusive_mouse(False)
                get_game().menu['pause'].frame.enable()
                if self._data['die']:
                    get_game().close()
        elif symbol == key.TAB:
            if self._data['gamemode'] != 1:
                self._data['flying'] = not self._data['flying']
        elif symbol == key.LSHIFT:
            if self._data['flying']:
                self._data['dy'] = -0.1 * JUMP_SPEED
            else:
                self._data['stealing'] = True
        elif symbol == key.LCTRL:
            if not self._data['flying']:
                self._data['running'] = True
        elif symbol in get_game().num_keys:
            self._data['block'] = (symbol - get_game().num_keys[0]) % len(get_game().inventory)
            get_game().hud['hotbar'].set_index(self._data['block'])
        elif symbol == key.F1:
            self._data['hide_hud'] = not self._data['hide_hud']
        elif symbol == key.F2:
            name = 'screenshot-%d.png' % int(time.time())
            pyglet.image.get_buffer_manager().get_color_buffer().save(os.path.join(
                path['screenshot'], name))
            self.dialogue.add_dialogue('screenshot saved in: %s' % name)
        elif symbol == key.F3:
            get_game().ext['enable'] = True
        elif symbol == key.F11:
            get_game().set_fullscreen(not get_game().fullscreen)

    def on_key_release(self, symbol, modifiers):
        if self._data['in_chat']:
            return
        if symbol == key.W:
            self._data['strafe'][0] += 1
        elif symbol == key.S:
            self._data['strafe'][0] -= 1
        elif symbol == key.A:
            self._data['strafe'][1] += 1
        elif symbol == key.D:
            self._data['strafe'][1] -= 1
        elif symbol == key.SPACE:
            if self._data['flying']:
                self._data['dy'] = 0
        elif symbol == key.LSHIFT:
            if self._data['flying']:
                self._data['dy'] = 0
            else:
                self._data['stealing'] = False
        elif symbol == key.LCTRL:
            self._data['running'] = False
        elif symbol == key.F3:
            get_game().ext['enable'] = False
