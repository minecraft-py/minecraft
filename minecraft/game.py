from difflib import get_close_matches
import math
import os
import random
import sys
import time
from threading import Thread
import traceback
import uuid

try:
    import pyglet
    from pyglet import image
    from pyglet.gl import *
    from pyglet.shapes import Rectangle
    from pyglet.sprite import Sprite
    from pyglet.window import key, mouse

    from minecraft.command.commands import commands
    from minecraft.gui.bag import Bag
    from minecraft.gui.dialogue import Dialogue
    from minecraft.gui.hotbar import HotBar
    from minecraft.gui.xpbar import XPBar
    from minecraft.gui.hud.heart import Heart
    from minecraft.gui.hud.hunger import Hunger
    from minecraft.gui.loading import Loading
    from minecraft.gui.guis import Chat, PauseMenu
    from minecraft.gui.widget.label import ColorLabel
    from minecraft.player import Player
    import minecraft.saves as saves
    from minecraft.source import libs, player, resource_pack, settings
    from minecraft.world.block import blocks, get_block_icon
    from minecraft.world.sky import change_sky_color
    from minecraft.world.weather import weather, choice_weather
    from minecraft.world.world import World
    from minecraft.utils.utils import *

    import psutil
    import pyshaders
    import opensimplex
except (Exception, ImportError, ModuleNotFoundError) as err:
    print('[ERR  %s client] Some dependencies are not installed' % time.strftime('%H:%M:%S'))
    traceback.print_exc()
    exit(1)


class Game(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 是否初始化
        self.is_init = True
        # 窗口是否捕获鼠标
        self.exclusive = False
        # 玩家所处的区域
        self.sector = None
        # 游戏世界(秒)
        self.time = 0
        # 玩家
        self.player = Player()
        # 键盘/鼠标事件
        self.event = dict()
        # HUD/GUI
        self.hud = dict()
        self.guis = dict()
        # 显示在 debug 区域的 info
        self._info_ext = list()
        self._info_ext.append('pyglet' + pyglet.version)
        # 拓展功能
        self.debug = dict(debug=False, enable=False)
        # 天气(现在天气, 持续时间)
        self.weather = {'now': 'clear', 'duration': 0}
        # 玩家可以放置的方块, 使用数字键切换
        self.inventory = ['grass', 'dirt', 'log', 'brick', 'leaf', 'plank', 'craft_table', 'glass']
        self.inventory += [None] * (9 - len(self.inventory))
        # 数字键列表
        self.num_keys = [key._1, key._2, key._3, key._4, key._5, key._6, key._7, key._8, key._9, key._0]
        # 加载窗口
        self.loading = Loading()
        # 聊天区
        self.dialogue = Dialogue()
        # 设置图标
        self.set_icon(get_block_icon(blocks['craft_table'], 64))
        # 窗口最小为 800x600
        self.set_minimum_size(800, 600)
        # 这个十字在屏幕中央
        self.reticle = Sprite(resource_pack.get_resource('textures/gui/icons').get_region(0, 240, 16, 16))
        self.reticle.image.anchor_x = 8
        self.reticle.image.anchor_y = 8
        self.reticle.scale = 2
        self.label = dict()
        # 这个标签在画布的上方显示
        self.label['top'] = ColorLabel('',
            x=2, y=self.height - 5, width=self.width // 2, multiline=True,
            anchor_x='left', anchor_y='top', font_size=16)
        # 这个标签在画布正中偏上显示
        self.label['title'] = ColorLabel('',
            x=self.width // 2, y=self.height // 2 + 50, anchor_x='center',
            anchor_y='center')
        # 这个标签在画布正中偏下显示
        self.label['subtitle'] = ColorLabel('',
                x=self.width // 2, y=self.height // 2 - 100, anchor_x='center', anchor_y='center')
        # 这个标签在画布正中再偏下一点显示
        self.label['actionbar'] = ColorLabel('',
                x=self.width // 2, y=self.height // 2 - 150, anchor_x='center', anchor_y='center')
        # 死亡信息
        self.die_info = ColorLabel('', color='white',
            x=self.width // 2, y=self.height // 2, anchor_x='center',
            anchor_y='center', font_size=24) 
        # 覆盖屏幕的矩形
        self.full_screen = Rectangle(0, 0, self.width, self.height)
        # 将 self.upgrade() 方法每 1.0 / TICKS_PER_SEC 调用一次, 它是游戏的主事件循环
        pyglet.clock.schedule_interval(self.update, 1.0 / TICKS_PER_SEC)
        # 每1/10秒更新一次方块数据
        pyglet.clock.schedule_interval(self.update_status, 0.1)
        # 每30秒保存一次进度
        pyglet.clock.schedule_interval(self.save, 30.0)
        # 天空颜色变换
        pyglet.clock.schedule_interval(change_sky_color, 7.5)
        log_info('Welcome %s' % player['name'])
        for lib in libs:
            if hasattr(lib, 'main'):
                lib.main()

    def can_place(self, block, position):
        """
        检测坐标是否能够放置方块

        :param: block 方块坐标
        :param: position 玩家坐标
        """
        if block != normalize(position):
            position = position[0], position[1] - 1, position[2]
            if block != normalize(position):
                return True
            else:
                return False
        else:
            return False

    def add_info_ext(self, s):
        self._info_ext.append(s)

    def check_die(self, dt):
        """
        这个函数被 pyglet 计时器反复调用

        :param: dt 距上次调用的时间
        """
        if not self.player['die']:
            if self.player['position'][1] < -64:
                self.player['die_reason'] = resource_pack.get_translation('game.text.die.fall_into_void') % player['name']
                self.player['die'] = True
                self.dialogue.add_dialogue(self.player['die_reason'])
            elif self.player['position'][1] > 512:
                self.player['die_reason'] = resource_pack.get_translation('game.text.die.no_oxygen') % player['name']
                self.player['die'] = True
            if self.player['die']:
                log_info('%s die: %s' % (player['name'], self.player['die_reason']))
                self.dialogue.add_dialogue(self.player['die_reason'])
                self.set_exclusive_mouse(False)

    def init_gui(self):
        # 生命值
        self.hud['heart'] = Heart()
        # 饥饿值
        self.hud['hunger'] = Hunger()
        # 工具栏
        self.hud['hotbar'] = HotBar()
        self.hud['hotbar'].set_all(self.inventory)
        self.hud['hotbar'].set_index(self.player['now_block'])
        # 经验条
        self.hud['xpbar'] = XPBar()
        # GUI
        self.active_gui = None
        self.guis['bag'] = Bag(self)
        self.guis['chat'] = Chat(self)
        self.guis['pause'] = PauseMenu(self)
        self.toggle_gui('pause')

    def toggle_gui(self, name=''):
        if (name == '') or (self.player['active_gui'] == name):
            self.set_exclusive_mouse(True)
            self.player['in_gui'] = False
            self.player['active_gui'] = ''
            self.active_gui.frame.enable(False)
        else:
            if self.player['in_gui']:
                return
            self.set_exclusive_mouse(False)
            self.player['in_gui'] = True
            self.player['active_gui'] = name
            self.active_gui = self.guis[name]
            self.active_gui.frame.enable(True)

    def save(self, dt):
        """
        这个函数被 pyglet 计时器反复调用

        :param: dt 距上次调用的时间
        """
        saves.save_block(self.name, self.world.change)
        saves.save_player(self.name, self.player['position'], self.player['respawn_position'],
                normalize(self.player['rotation']), self.player['now_block'])
        saves.save_level(self.name, self.time, self.weather)

    def set_exclusive_mouse(self, exclusive):
        # 如果 exclusive 为 True, 窗口会捕获鼠标. 否则忽略之
        super(Game, self).set_exclusive_mouse(exclusive)
        self.exclusive = exclusive
        if not exclusive:
            self.set_cursor()

    def set_name(self, name):
        # 设置游戏存档名
        self.name = name
        self.world = World(name)
        # 读取玩家位置和背包
        data = saves.load_player(self.name)
        self.player['position'] = data['position']
        self.player['respawn_position'] = data['respawn']
        if len(self.player['position']) != 3:
            if saves.load_level(self.name)['type'] == 'flat':
                self.player['position'] = self.player['respawn_position'] = (0, 8, 0)
            else:
                self.player['position'] = self.player['respawn_position'] = (0, self.world.simplex.noise2d(x=0, y=0) * 5 + 13, 0)
        self.sector = sectorize(self.player['position'])
        self.player['rotation'] = tuple(data['rotation'])
        self.player['now_block'] = data['now_block']
        # 读取世界数据
        self.world_level = saves.load_level(self.name)
        self.time = self.world_level['time']
        self.weather = self.world_level['weather']
        weather[self.weather['now']].change()

    def set_cursor(self, cursor=None):
        # 设置光标形状
        self.set_mouse_cursor(self.get_system_mouse_cursor(cursor))

    def register_event(self, event, func):
        # 注册事件
        if ('on_%s' % event) not in self.event:
            self.event.setdefault('on_%s' % event, {str(uuid.uuid4()): func})
        else:
            self.event.get('on_%s' % event).setdefault(str(uuid.uuid4()), func)
        return (event, name)

    def remove_event(self, index):
        # 删除事件
        # 参数为 register_event 返回值
        del self.event['on_%s' % index[0]][index[1]]

    def run_command(self, s):
        # 运行命令
        command = s.split(' ')[0]
        if command not in commands:
            match = get_close_matches(s, list(commands.keys()), n=1)
            if len(match) == 1:
                self.dialogue.add_dialogue(resource_pack.get_translation('command.not_found')[1] % (command, match[0]))
            else:
                self.dialogue.add_dialogue(resource_pack.get_translation('command.not_found')[0] % command)
        else:
            try:
                log_info('Run command: %s' % s)
                cmd = commands[command](self, s)
            except TypeError as error:
                self.dialogue.add_dialogue('Arguments error: %s' % error.args[0])
            else:
                cmd.execute()

    def update(self, dt):
        """
        这个方法被 pyglet 计时器反复调用

        :param: dt 距上次调用的时间
        """
        self.world.process_queue()
        self.dialogue.update()
        sector = sectorize(self.player['position'])
        self.time += dt
        self.weather['duration'] -= dt
        if self.weather['duration'] <= 0:
            weather[self.weather['now']].leave()
            self.weather['now'] = choice_weather()
            weather[self.weather['now']].change()
            self.weather['duration'] = random.randint(*weather[self.weather['now']].duration)
            weather[self.weather['now']].update(dt)
        else:
            weather[self.weather['now']].update(dt)
        if sector != self.sector:
            self.world.change_chunk(self.sector, sector)
            if self.sector is None:
                self.world.process_entire_queue()
            self.sector = sector
        if (not self.player['in_gui']) or (self.player['dy'] !=0):
            m = 24
            dt = min(dt, 0.2)
            for _ in range(m):
                self._update(dt / m)

    def update_status(self, dt):
        # 这个函数定时改变世界状态
        for sector in self.world.sectors.values():
            if sector:
                blocks = random.choices(sector, k=3)
                for block in blocks:
                    self.world.get(block).on_ticking(block)

    def _update(self, dt):
        """
        update() 方法的私有实现, 刷新

        :param: dt 距上次调要用的时间
        """
        # 移动速度
        if self.player['flying']:
            speed = FLYING_SPEED
        elif self.player['running']:
            speed = RUNNING_SPEED
        elif self.player['stealing']:
            speed = STEALING_SPEED
        else:
            speed = WALKING_SPEED
        # 一个游戏刻玩家经过的距离
        d = dt * speed
        dx, dy, dz = self.player.get_motion_vector()
        # 玩家新的位置
        dx, dy, dz = dx * d, dy * d, dz * d
        # 重力
        if (not self.player['flying']):
            self.player['dy'] -= dt * GRAVITY
            self.player['dy'] = max(self.player['dy'], -TERMINAL_VELOCITY)
            dy += self.player['dy'] * dt
        if (not self.player['die']) or (self.player['dy'] != 0):
            x, y, z = self.player['position']
            if self.player['gamemode'] != 1:
                x, y, z = self.player.collide((x + dx, y + dy, z + dz))
            else:
                x, y, z = x + dx, y + dy, z + dz
            self.player['position'] = (x, y, z)

    def on_close(self):
        # 当玩家关闭窗口时调用
        saves.save_window(self.width, self.height)
        pyglet.app.exit()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        当玩家按下鼠标按键时调用

        :param: x, y 鼠标点击时的坐标, 如果被捕获的话总是在屏幕中央
        :param: button 哪个按键被按下: 1 = 左键, 4 = 右键
        :param: modifiers 表示单击鼠标按钮时按下的任何修改键的数字
        """
        self.active_gui.frame.on_mouse_press(x, y, button, modifiers)
        self.player.on_mouse_press(x, y, button, modifiers)
        for func in self.event.get('on_mouse_press', {}).values():
            func(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.active_gui.frame.on_mouse_release(x, y, button, modifiers)
        for func in self.event.get('on_mouse_release', {}).values():
            func(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        """
        当玩家移动鼠标时调用

        :param: x, y 鼠标点击时的坐标, 如果被捕获的话它们总是在屏幕中央
        :param: dx, dy 鼠标移动的距离
        """
        self.active_gui.frame.on_mouse_motion(x, y, dx, dy)
        self.player.on_mouse_motion(x, y, dx, dy)
        for func in self.event.get('on_mouse_motion', {}).values():
            func(x, y, dx, dy)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        """
        当鼠标滚轮滚动时调用

        :param: scroll_x, scroll_y 鼠标滚轮滚动(scroll_y 为1时向上, 为-1时向下)
        """
        self.active_gui.frame.on_mouse_scroll(x, y, scroll_x, scroll_y)
        self.player.on_mouse_scroll(x, y, scroll_x, scroll_y)
        for func in self.event.get('on_mouse_scroll', {}).values():
            func(x, y, scroll_x, scroll_y)

    def on_key_press(self, symbol, modifiers):
        """
        当玩家按下一个按键时调用

        :param: symbol 按下的键
        :param: modifiers 同时按下的修饰键
        """
        self.active_gui.frame.on_key_press(symbol, modifiers)
        self.player.on_key_press(symbol, modifiers)
        for func in self.event.get('on_key_press', {}).values():
            func(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        """
        当玩家释放一个按键时调用

        :param: symbol 释放的键
        """
        self.active_gui.frame.on_key_release(symbol, modifiers)
        self.player.on_key_release(symbol, modifiers)
        for func in self.event.get('on_mouse_release', {}).values():
            func(symbol, modifiers)

    def on_resize(self, width, height):
        # 当窗口被调整到一个新的宽度和高度时调用
        # 标签
        self.label['top'].x = 2
        self.label['top'].y = self.height - 5
        self.label['top'].width = self.width / 2
        self.label['title'].x = self.width / 2
        self.label['title'].y = self.height / 2 + 50
        self.label['subtitle'].x = self.width / 2
        self.label['subtitle'].y = self.height / 2 - 100
        self.label['actionbar'].x = self.width / 2
        self.label['actionbar'].y = self.height / 2 - 150
        self.die_info.x = self.width / 2
        self.die_info.y = self.height / 2
        # 加载窗口
        self.loading.resize(self.width, self.height)
        # 窗口中央的十字线
        self.reticle.position = (self.width / 2, self.height / 2)
        # 覆盖屏幕的矩形
        self.full_screen.position = (0, 0)
        self.full_screen.width = self.width
        self.full_screen.height = self.height
        # 聊天区
        self.dialogue.resize(self.width, self.height)
        # 在第一次调用该函数时, 所有存储 GUI 的变量都没有定义
        if not self.is_init:
            self.hud['heart'].resize(self.width, self.height)
            self.hud['hunger'].resize(self.width, self.height)
            self.hud['hotbar'].resize(self.width, self.height)
            self.hud['xpbar'].resize(self.width, self.height)
            self.active_gui.frame.on_resize(width, height)
            for func in self.event.get('on_resize', {}).values():
                func(width, height)

    def set_2d(self):
        # 使 OpenGL 绘制二维图形
        width, height = self.get_size()
        glDisable(GL_DEPTH_TEST)
        viewport = self.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, max(1, width), 0, max(1, height), -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set_3d(self):
        # 使 OpenGL 绘制三维图形
        width, height = self.get_size()
        glEnable(GL_DEPTH_TEST)
        viewport = self.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.player['fov'], width / float(height), 0.1, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x, y = self.player['rotation']
        glRotatef(x, 0, 1, 0)
        glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))
        x, y, z = self.player['position']
        glTranslatef(-x, -y + (0.1 if self.player['stealing'] else 0), -z)

    def on_draw(self):
        # 当 pyglet 在画布上绘图时调用
        self.clear()
        if not self.is_init:
            self.set_3d()
            glColor3d(1, 1, 1)
            self.world.draw()
            self.draw_focused_block()
            weather[self.weather['now']].draw()
            self.set_2d()
            if not self.player['die'] and not self.player['hide_hud']:
                if self.player['gamemode'] != 1:
                    self.hud['hotbar'].draw()
                if not self.player['in_gui']:
                    self.reticle.draw()
                if self.player['in_gui']:
                    self.active_gui.frame.draw()
            elif self.player['die']:
                self.full_screen.color = (200, 0, 0)
                self.full_screen.opacity = 100
                self.full_screen.draw()
            if not self.player['hide_hud']:
                self.draw_label()
            for func in self.event.get('on_draw', {}).values():
                func()
        if self.is_init:
            self.world.init_world()
            self.init_gui()
            for func in self.event.get('on_init', {}).values():
                func()
            self.is_init = False

    def on_text(self, text):
        self.active_gui.frame.on_text(text)

    def on_text_motion(self, motion):
        self.active_gui.frame.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        self.active_gui.frame.on_text_motion_select(motion)

    def draw_focused_block(self):
        # 在十字线选中的方块绘制黑框
        vector = self.player.get_sight_vector()
        block = self.world.hit_test(self.player['position'], vector)[0]
        if block and self.player['gamemode'] != 1:
            x, y, z = block
            vertex_data = cube_vertices(x, y, z, 0.501)
            glColor3f(0.0, 0.0, 0.0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glLineWidth(1.5)
            glDisable(GL_CULL_FACE)
            pyglet.graphics.draw(24, GL_QUADS, ('v3f/static', vertex_data))
            glEnable(GL_CULL_FACE)
            glLineWidth(1.0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def draw_label(self):
        if not self.is_init:
            if self.exclusive:
                self.dialogue.draw()
            if self.player['die']:
                # 玩家死亡
                self.die_info.text = resource_pack.get_translation('game.text.die')
                self.label['actionbar'].text = self.player['die_reason']
                self.die_info.draw()
                self.label['actionbar'].draw()
            elif self.debug['debug'] and self.exclusive:
                x, y, z = self.player['position']
                rx, ry = self.player['rotation']
                mem = round(psutil.Process(os.getpid()).memory_full_info()[0] / 1048576, 2)
                fps = pyglet.clock.get_fps()
                text = '\n'.join(resource_pack.get_translation('game.text.debug'))
                text = text.replace('%(version)', VERSION['str']).replace('%(info)', ', '.join(self._info_ext))
                text = text.replace('%(xyz)', '%.1f, %.1f, %.1f' % (x, y, z)).replace('%(rot)', '%.2f, %.2f' % (rx, ry))
                text = text.replace('%(mem)', '%.2f' % mem).replace('%(fps)', '%d' % fps)
                self.label['top'].text = text
                self.label['top'].draw()
        else:
            # 初始化屏幕
            self.loading.draw()

