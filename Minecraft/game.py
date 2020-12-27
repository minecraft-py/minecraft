import math
import os
import random
import sys
import time
from threading import Thread

import Minecraft.archiver as archiver
from Minecraft.source import path, player, lang, settings
from Minecraft.gui.bag import Bag
from Minecraft.gui.dialogue import Dialogue
from Minecraft.gui.hotbar import HotBar
from Minecraft.gui.xpbar import XPBar
from Minecraft.gui.hud.heart import Heart
from Minecraft.gui.hud.hunger import Hunger
from Minecraft.gui.loading import Loading
from Minecraft.menu import PauseMenu
from Minecraft.world.block import blocks
from Minecraft.world.sky import change_sky_color, get_time, set_time
from Minecraft.world.world import World
from Minecraft.utils.utils import *

msg = "module '{0}' not found, run `pip install {0}` to install, exit"

try:
    import js2py as js
except ModuleNotFoundError:
    log_err(msg.format('Js2Py'))
    exit(1)

try:
    import pyglet
    from pyglet import image
    from pyglet.gl import *
    from pyglet.shapes import Rectangle
    from pyglet.text import decode_attributed
    from pyglet.window import key, mouse
except:
    log_err(msg.format('pyglet'))
    exit(1)

try:
    import psutil
except:
    log_err(msg.format('psutil'))
    exit(1)

try:
    import pyshaders
except:
    log_err(msg.format('pyshaders'))
    exit(1)


class Game(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)
        # 窗口是否捕获鼠标
        self.exclusive = False
        # 玩家状态: 是否潜行, 是否飞行...
        self.player = {}
        self.player['stealing'] = False
        self.player['flying'] = False
        self.player['running'] = False
        self.player['die'] = False
        self.player['in_hud'] = False
        self.player['hide_hud'] = False
        self.player['show_bag'] = False
        # strafe = [z, x]
        # z 代表前后运动
        # x 代表左右运动
        self.player['strafe'] = [0, 0]
        # 玩家在世界中的位置 (x, y, z)
        self.player['position'] = (0, 4, 0)
        self.player['respawn_position'] = (0, 4, 0)
        # 玩家视角场
        self.player['fov'] = settings['fov']
        # 拓展功能
        self.ext = {}
        self.ext['debug'] = False
        self.ext['enable'] = False
        self.ext['position'] = False
        self.ext['running'] = False
        # rotation = (水平角 x, 俯仰角 y)
        self.player['rotation'] = (0, 0)
        # 玩家所处的区域
        self.sector = None
        # 这个十字在屏幕中央
        self.reticle = None
        # y 轴的加速度
        self.dy = 0
        # 玩家可以放置的方块, 使用数字键切换
        self.inventory = ['grass', 'dirt', 'log', 'brick', 'leaf', 'plank', 'glass', 'craft_table']
        # 玩家手持的方块
        self.block = 0
        # 数字键列表
        self.num_keys = [
            key._1, key._2, key._3, key._4, key._5,
            key._6, key._7, key._8, key._9, key._0]
        # 这个标签在画布的上方显示
        self.label = {}
        self.label['top'] = pyglet.text.DocumentLabel(decode_attributed(''),
            x=0, y=self.height - 30,width=self.width // 2, multiline=True,
            anchor_x='left', anchor_y='center')
        self.is_init = True
        # 这个标签在画布正中偏上显示
        self.label['center'] = pyglet.text.DocumentLabel(decode_attributed(''),
            x=self.width // 2, y=self.height // 2 + 50, anchor_x='center',
            anchor_y='center')
        # 这个标签在画布正中偏下显示
        self.label['actionbar'] = pyglet.text.DocumentLabel(decode_attributed(''),
                x=self.width // 2, y=self.height // 2 - 100, anchor_x='center', anchor_y='center')
        # 加载窗口
        self.loading = Loading()
        # 覆盖屏幕的矩形
        self.full_screen = Rectangle(0, 0, self.width, self.height)
        # 聊天区
        self.dialogue = Dialogue()
        # 将 self.upgrade() 方法每 1.0 / TICKS_PER_SEC 调用一次, 它是游戏的主事件循环
        pyglet.clock.schedule_interval(self.update, 1.0 / TICKS_PER_SEC)
        # 检测玩家是否应该死亡
        pyglet.clock.schedule_interval(self.check_die, 1.0 / TICKS_PER_SEC)
        # 每10秒更新一次方块数据
        pyglet.clock.schedule_interval(self.update_status, 10.0)
        # 每30秒保存一次进度
        pyglet.clock.schedule_interval(self.save, 30.0)
        # 天空颜色变换
        pyglet.clock.schedule_interval(change_sky_color, 7.5)
        # 设置图标
        self.set_icon(image.load(os.path.join(path['texture'], 'icon.png')))
        log_info('welcome %s' % player['name'])

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

    def check_die(self, dt):
        """
        这个函数被 pyglet 计时器反复调用

        :param: dt 距上次调用的时间
        """
        return
        if not self.player['die']:
            if self.player['position'][1] < -64:
                self.player['die_reason'] = lang['game.text.die.fall_into_void'] % player['name']
                self.player['die'] = True
                self.dialogue.add_dialogue(self.player['die_reason']) 
            elif self.player['position'][1] > 512:
                self.player['die_reason'] = lang['game.text.die.no_oxygen'] % player['name']
                self.player['die'] = True
            if self.player['die']:
                log_info('%s die: %s' % (player['name'], self.player['die_reason']))
                self.dialogue.add_dialogue(self.player['die_reason'])
                self.set_exclusive_mouse(False)

    def init_player(self):
        # 初始化玩家
        self.hud = {}
        # E 键打开的背包
        self.hud['bag'] = Bag()
        # 生命值
        self.hud['heart'] = Heart(batch=self.world.batch2d)
        # 饥饿值
        self.hud['hunger'] = Hunger(batch=self.world.batch2d)
        # 工具栏
        self.hud['hotbar'] = HotBar()
        self.hud['hotbar'].set_index(self.block)
        self.hud['hotbar'].set_all(self.inventory)
        # 经验条
        self.hud['xpbar'] = XPBar()
        # 菜单
        self.menu = {}
        self.menu['pause'] = PauseMenu(self)
        self.menu['pause'].frame.enable(True)
        
    def save(self, dt):
        """
        这个函数被 pyglet 计时器反复调用

        :param: dt 距上次调用的时间
        """
        # archiver.save_block(self.name, self.world.change)
        archiver.save_player(self.name, self.player['position'], self.player['respawn_position'], self.block)
        archiver.save_info(self.name, 0, get_time())

    def set_exclusive_mouse(self, exclusive):
        # 如果 exclusive 为 True, 窗口会捕获鼠标. 否则忽略之
        super(Game, self).set_exclusive_mouse(exclusive)
        self.exclusive = exclusive

    def _js_addBlock(self, x, y, z, block):
        # addBlock 的 javascript 函数定义
        if block == 'air':
            self.world.remove_block((x, y, z))
        else:
            self.world.add_block((x, y, z), block)

    def _js_getBlock(self, x, y, z):
        # getBlock 的 javascript 函数定义
        if self.world.get((x, y, z)) is not None:
            return self.world.get((x, y, z))
        else:
            return 'air'

    def _js_getGLlib(self, s):
        # getGLlib 的 javascript 函数定义
        if hasattr(pyglet.gl, s):
            return getattr(pyglet.gl, s)
        else:
            return None

    def _js_getSettings(self, key):
        # getSettings 的 javascript 函数定义
        if key.find('.') == -1:
            if key in settings:
                return settings[key]
            else:
                return None
        else:
            key = key.split('.')
            item = None
            for i in key:
                if i in settings:
                    item = settings[i]
                else:
                    return None
            else:
                return None

    def _js_loadGLlib(self, s):
        # loadGLlib 的 javascript 函数定义
        self.js.eval('%s = getGLlib("%s");' % (s, s))

    def _js_logInfo(self, s):
        # logInfo 的 javascript 函数定义
        log_info(s)

    def _js_logErr(self, s):
        # logErr 的 javascript 函数定义
        log_err(s)

    def _js_logWarn(self, s):
        # logWarn 的 javascript 函数定义
        log_warn(s)

    def _js_message(self, s):
        # message 的 javascript 函数定义
        self.dialogue.add_dialogue(s)
    
    def _js_removeBlock(self, x, y, z):
        # removeBlock 的 javascript 函数定义
        self.world.remove_block((x, y, z))

    def _js_testBlock(self, x, y, z, block):
        # testBlock 的 javascript 函数定义
        if (x, y, z) not in self.world.world and block != 'air':
            return False
        elif (x, y, z) not in self.world.world and block == 'air':
            return True
        elif self.world.world[(x, y, z)].name != block:
            return False
        else:
            return True
        
    def set_name(self, name):
        # 设置游戏存档名
        self.name = name
        self.world = World(name, self)
        # self.world_gen_thread = Thread(target=self.world.init_world, name='WorldGen')
        # self.world_gen_thread.start()
        # 读取玩家位置和背包
        data = archiver.load_player(self.name)
        self.player['position'] = data['position']
        self.sector = sectorize(self.player['position'])
        self.player['respawn_position'] = data['respawn']
        self.block = data['now_block']
        # 读取世界数据
        self.world_info = archiver.load_info(self.name)
        set_time(self.world_info['time'])
        # 读取 js 脚本
        if os.path.isfile(os.path.join(path['mcpypath'], 'save', name, 'script.js')):
            self.has_script = True
            self.js = js.EvalJs({
                    'addBlock': self._js_addBlock,
                    'getBlock': self._js_getBlock,
                    'getGLlib': self._js_getGLlib,
                    'getSettings': self._js_getSettings,
                    'loadGLlib': self._js_loadGLlib,
                    'logInfo': self._js_logInfo,
                    'logErr': self._js_logErr,
                    'logWarn': self._js_logWarn,
                    'message': self._js_message,
                    'removeBlock': self._js_removeBlock,
                    'testBlock': self._js_testBlock
                }, enable_require=True)
            try:
                self.js.eval(open(os.path.join(path['mcpypath'], 'save', name, 'script.js')).read())
            except Exception as err:
                log_err('script.js: %s' % str(err))
                exit(1)
        else:
            self.has_script = False

    def run_js(self, function, *args):
        # NOTE: 实验性
        if self.has_script and hasattr(self, 'js'):
            try:
                if hasattr(self.js, function):
                    # NOTE: Js2Py.EvalJs 对象的 hasattr 方法有漏洞!
                    func = getattr(self.js, function)
                    return func(*args)
            except Exception as err:
                log_err('javascript: %s: %s' % (function, str(err)))

    def get_sight_vector(self):
        # 返回玩家的视线方向
        x, y = self.player['rotation']
        # y 的范围为 -90 到 90, 或 -pi/2 到 pi/2.
        # 所以 m 的范围为 0 到 1
        m = math.cos(math.radians(y))
        # dy 的范围为 -1 到 1. 玩家向下看为 -1, 向上看为 1
        dy = math.sin(math.radians(y))
        dx = math.cos(math.radians(x - 90)) * m
        dz = math.sin(math.radians(x - 90)) * m
        return (dx, dy, dz)

    def get_motion_vector(self):
        """
        计算运动时3个轴的位移增量

        :return: 长度为3的元组, 包含 x, y, z 轴上的速度增量
        """
        dy = dx = dz = 0.0
        x, y = self.player['rotation']
        strafe = math.degrees(math.atan2(*self.player['strafe']))
        y_angle = math.radians(y)
        x_angle = math.radians(x + strafe)
        if any(self.player['strafe']):
            if self.player['flying']:
                dx = math.cos(x_angle)
                dy = 0.0
                dz = math.sin(x_angle)
            else:
                dy = 0.0
                dx = math.cos(x_angle)
                dz = math.sin(x_angle)
        elif self.player['flying'] and not self.dy == 0:
            dx = 0.0
            dy = self.dy
            dz = 0.0
        return (dx, dy, dz)

    def update(self, dt):
        """
        这个方法被 pyglet 计时器反复调用

        :param: dt 距上次调用的时间
        """
        self.world.process_queue()
        self.dialogue.update()
        sector = sectorize(self.player['position'])
        if sector != self.sector:
            self.world.change_chunk(self.sector, sector)
            if self.sector is None:
                self.world.process_entire_queue()
            self.sector = sector
        m = 8
        dt = min(dt, 0.2)
        for _ in range(m):
            self._update(dt / m)

    def update_status(self, dt):
        # 这个函数定时改变世界状态
        area = []
        for x in range(int(self.player['position'][0]) - 16, int(self.player['position'][0]) + 17):
            for y in range(int(self.player['position'][1]) - 2, int(self.player['position'][1]) + 3):
                for z in range(int(self.player['position'][2]) - 16, int(self.player['position'][2]) + 17):
                    # 以玩家为中心的 32*32*4 范围
                    area.append((x, y, z))
        else:
            for position in [exist for exist in area if self.world.get(exist) is not None]:
                block = self.world.get(position)
                if block.name == 'dirt' and random.randint(0, 10) == 10:
                    for x, z in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        pos = (position[0] + x, position[1], position[2] + z)
                        if self.world.get(pos) is not None:
                            if self.world.get(pos).name == 'grass' and self.world.get((pos[0], pos[1] + 1, pos[2])) is None:
                                self.world.add_block(position, 'grass')
                elif block.name == 'grass':
                    if self.world.get((position[0], position[1] + 1, position[2])) is not None:
                        self.world.add_block(position, 'dirt')
            
    def _update(self, dt):
        """
        update() 方法的私有实现, 刷新 
        
        :param: dt 距上次调要用的时间
        """
        # 移动速度
        if self.player['flying']:
            speed = FLYING_SPEED
        elif self.player['running'] or self.ext['running']:
            speed = RUNNING_SPEED
        elif self.player['stealing']:
            speed = STEALING_SPEED
        else:
            speed = WALKING_SPEED
        # 一个游戏刻玩家经过的距离
        d = dt * speed
        dx, dy, dz = self.get_motion_vector()
        # 玩家新的位置
        dx, dy, dz = dx * d, dy * d, dz * d
        # 重力
        if not self.player['die']:
            if not self.player['flying']:
                self.dy -= dt * GRAVITY
                self.dy = max(self.dy, -TERMINAL_VELOCITY)
                dy += self.dy * dt
            if not self.player['in_hud']:
                # 碰撞检测
                x, y, z = self.player['position']
                x, y, z = self.collide((x + dx, y + dy, z + dz), PLAYER_HEIGHT)
                self.player['position'] = (x, y, z)

    def collide(self, position, height):
        """
        碰撞检测

        :param: position, 玩家位置
        :param: height 玩家的高度
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
                for dy in range(height):
                    op = list(np)
                    op[1] -= dy
                    op[i] += face[i]
                    if self.world.get(tuple(op)) is None:
                        continue
                    p[i] -= (d - pad) * face[i]
                    if face == (0, -1, 0) or face == (0, 1, 0):
                        self.dy = 0
                    break
        else:
            return tuple(p)

    def on_close(self):
        # 当玩家关闭窗口时调用
        archiver.save_window(self.width, self.height)
        pyglet.app.exit()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        当玩家按下鼠标按键时调用
  
        :param: x, y 鼠标点击时的坐标, 如果被捕获的话总是在屏幕中央
        :param: button 哪个按键被按下: 1 = 左键, 4 = 右键
        :param: modifiers 表示单击鼠标按钮时按下的任何修改键的数字
        """
        for menu in self.menu.values():
            if menu.frame.on_mouse_press(x, y, button, modifiers):
                return
        if self.exclusive:
            vector = self.get_sight_vector()
            now, previous = self.world.hit_test(self.player['position'], vector)
            if now:
                block = self.world.get(now)
            else:
                return
            if (button == mouse.RIGHT) or ((button == mouse.LEFT) and (modifiers & key.MOD_CTRL)) and now and previous:
                # 在 Mac OS X 中, Ctrl + 左键 = 右键
                if not self.player['die'] and not self.player['in_hud']:
                    if hasattr(block, 'on_use') and (not self.player['stealing']):
                        block.on_use(self)
                    elif previous and self.can_place(previous, self.player['position']):
                        self.world.add_block(previous, self.inventory[self.block])
            elif button == pyglet.window.mouse.LEFT and previous:
                if block.hardness > 0 and not self.player['die'] and not self.player['in_hud']:
                    self.world.remove_block(now)
            elif button == pyglet.window.mouse.MIDDLE and block and previous:
                pass
        elif not self.player['die'] and not self.player['in_hud']:
            pass
        
    def on_mouse_release(self, x, y, button, modifiers):
        for menu in self.menu.values():
            menu.frame.on_mouse_release(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        """
        当玩家移动鼠标时调用

        :param: x, y 鼠标点击时的坐标, 如果被捕获的话它们总是在屏幕中央
        :param: dx, dy 鼠标移动的距离
        """
        for menu in self.menu.values():
            menu.frame.on_mouse_motion(x, y, dx, dy)
        if self.exclusive and not self.player['die']:
            m = 0.1
            x, y = self.player['rotation']
            x, y = x + dx * m, y + dy * m
            if x >= 180:
                x = -180
            elif x <= -180:
                x = 180
            y = max(-90, min(90, y))
            self.player['rotation'] = (x, y)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        """
        当鼠标滚轮滚动时调用

        :param: scroll_x, scroll_y 鼠标滚轮滚动(scroll_y 为1时向上, 为-1时向下)
        """
        index = int(self.block + scroll_y)
        if index > len(self.inventory) - 1:
            self.block = index = 0
        elif index < 0:
            self.block = index = len(self.inventory) - 1
        else:
            self.block = index
        self.hud['hotbar'].set_index(index)

    def on_key_press(self, symbol, modifiers):
        """
        当玩家按下一个按键时调用

        :param: symbol 按下的键
        :param: modifiers 同时按下的修饰键
        """
        if symbol == key.Q:
            self.player['die'] = True
            self.player['die_reason'] = 'killed by self'
            self.set_exclusive_mouse(False)
        if symbol == key.W:
            self.player['strafe'][0] -= 1
        elif symbol == key.S:
            self.player['strafe'][0] += 1
        elif symbol == key.A:
            self.player['strafe'][1] -= 1
        elif symbol == key.D:
            self.player['strafe'][1] += 1
        elif symbol == key.I:
             if self.ext['enable']:
                self.ext['debug'] = not self.ext['debug']
                self.ext['position'] = False
        elif symbol == key.E:
            if not self.player['die']:
                self.set_exclusive_mouse(self.player['show_bag'])
                self.player['in_hud'] = not self.player['in_hud']
                self.player['show_bag'] = not self.player['show_bag']
        elif symbol == key.P:
            if self.ext['enable']:
                self.ext['position'] = not self.ext['position']
                self.ext['debug'] = False
        elif symbol == key.R:
            if self.ext['enable']:
                self.ext['running'] = not self.ext['running']
        elif symbol == key.SPACE:
            if self.player['flying']:
                self.dy = 0.1 * JUMP_SPEED
            elif self.dy == 0:
                self.dy = JUMP_SPEED
        elif symbol == key.ENTER:
            if self.player['die']:
                self.player['die'] = False
                self.player['position'] = self.player['respawn_position']
                self.set_exclusive_mouse(True)
        elif symbol == key.ESCAPE:
            self.save(0)
            self.set_exclusive_mouse(False)
            self.menu['pause'].frame.enable()
            if self.player['die']:
                self.close()
        elif symbol == key.TAB:
            self.player['flying'] = not self.player['flying']
        elif symbol == key.LSHIFT:
            if self.player['flying']:
                self.dy = -0.1 * JUMP_SPEED
            else:
                self.player['stealing'] = True
        elif symbol == key.LCTRL:
            if not self.player['flying']:
                self.player['running'] = True
        elif symbol in self.num_keys:
            self.block = (symbol - self.num_keys[0]) % len(self.inventory)
            self.hud['hotbar'].set_index(self.block)
        elif symbol == key.F1:
            self.player['hide_hud'] = not self.player['hide_hud']
        elif symbol == key.F2:
            name = 'screenshot-%d.png' % int(time.time())
            pyglet.image.get_buffer_manager().get_color_buffer().save(os.path.join(
                path['screenshot'], name))
            self.dialogue.add_dialogue('screenshot saved in: %s' % name)
        elif symbol == key.F3:
            self.ext['enable'] = True
        elif symbol == key.F11:
            self.set_fullscreen(not self.fullscreen)

    def on_key_release(self, symbol, modifiers):
        """
        当玩家释放一个按键时调用
        
        :param: symbol 释放的键
        """
        if symbol == key.W:
            self.player['strafe'][0] += 1
        elif symbol == key.S:
            self.player['strafe'][0] -= 1
        elif symbol == key.A:
            self.player['strafe'][1] += 1
        elif symbol == key.D:
            self.player['strafe'][1] -= 1
        elif symbol == key.SPACE:
            if self.player['flying']:
                self.dy = 0
        elif symbol == key.LSHIFT:
            if self.player['flying']:
                self.dy = 0
            else:
                self.player['stealing'] = False
        elif symbol == key.LCTRL:
            self.player['running'] = False
        elif symbol == key.F3:
            self.ext['enable'] = False

    def on_resize(self, width, height):
        # 当窗口被调整到一个新的宽度和高度时调用
        # 标签
        self.label['top'].x = 0
        self.label['top'].y = self.height - 10
        self.label['top'].width = self.width // 2
        self.label['center'].x = self.width // 2
        self.label['center'].y = self.height // 2 + 50
        self.label['actionbar'].x = self.width // 2
        self.label['actionbar'].y = self.height // 2 - 100
        # 加载窗口
        self.loading.resize(self.width, self.height)
        # 窗口中央的十字线
        if self.reticle:
            self.reticle.delete()
        x, y = self.width // 2, self.height // 2
        n = 12
        self.reticle = pyglet.graphics.vertex_list(4,
            ('v2i', (x - n, y, x + n, y, x, y - n, x, y + n))
        )
        # 覆盖屏幕的矩形
        self.full_screen.position = (0, 0)
        self.full_screen.width = self.width
        self.full_screen.height = self.height
        # 聊天区
        self.dialogue.resize(self.width, self.height)
        # HUD
        # 在第一次调用该函数时, 所有存储 HUD 的变量都没有定义
        if not self.is_init:
            self.hud['bag'].resize(self.width, self.height)
            self.hud['heart'].resize(self.width, self.height)
            self.hud['hunger'].resize(self.width, self.height)
            self.hud['hotbar'].resize(self.width, self.height)
            self.hud['xpbar'].resize(self.width, self.height)
            for menu in self.menu.values():
                menu.frame.on_resize(width, height)

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
            self.world.batch3d.draw()
            self.draw_focused_block()
            self.set_2d()
            if not self.player['die'] and not self.player['hide_hud']:
                self.world.batch2d.draw()
                self.hud['hotbar'].draw()
                self.hud['xpbar'].draw()
                self.draw_reticle()
                if not self.player['in_hud'] and not self.exclusive:
                    self.full_screen.color = (0, 0, 0)
                    self.full_screen.opacity = 100
                    self.full_screen.draw()
                    self.menu['pause'].frame.draw()
                if self.player['in_hud'] or not self.exclusive:
                    self.full_screen.color = (0, 0, 0)
                    self.full_screen.opacity = 100
                    self.full_screen.draw()
                    if self.player['show_bag']:
                        self.hud['bag'].draw()
            elif self.player['die']:
                self.full_screen.color = (200, 0, 0)
                self.full_screen.opacity = 100
                self.full_screen.draw()
        self.set_2d()
        if not self.player['hide_hud']:
            self.draw_label()
        if self.is_init:
            self.world.init_world()
            self.run_js('onInit')
            self.init_player()
            self.is_init = False

    def draw_focused_block(self):
        # 在十字线选中的方块绘制黑边
        vector = self.get_sight_vector()
        block = self.world.hit_test(self.player['position'], vector)[0]
        if block:
            x, y, z = block
            vertex_data = cube_vertices(x, y, z, 0.51)
            glColor3f(0.0, 0.0, 0.0)
            glLineWidth(1.5)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glDisable(GL_CULL_FACE)
            pyglet.graphics.draw(24, GL_QUADS, ('v3f/static', vertex_data))
            glEnable(GL_CULL_FACE)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glLineWidth(1.0)

    def draw_label(self):
        if not self.is_init:
            self.dialogue.draw()
            if self.player['die']:
                # 玩家死亡
                self.label['center'].document = decode_attributed('{color (255, 255, 255, 255)}{font_size 30}' +
                        lang['game.text.die'])
                self.label['actionbar'].document = decode_attributed('{color (0, 0, 0, 255)}{font_size 15}' +
                        self.player['die_reason'])
                self.label['center'].draw()
                self.label['actionbar'].draw()
            elif self.ext['position'] and self.exclusive:
                # 在屏幕左上角绘制标签
                x, y, z = self.player['position']
                self.label['top'].document = decode_attributed('{color (255, 255, 255, 255)}{background_color (0, 0, 0, 64)}' +
                        lang['game.text.position'] % (x, y, z, pyglet.clock.get_fps()))
                self.label['top'].draw()
            elif self.ext['debug'] and self.exclusive:
                x, y, z = self.player['position']
                rx, ry = self.player['rotation']
                mem = round(psutil.Process(os.getpid()).memory_full_info()[0] / 1048576, 2)
                fps = pyglet.clock.get_fps()
                self.label['top'].y = self.height - 60
                self.label['top'].document = decode_attributed('{color (255, 255, 255, 255)}{background_color (0, 0, 0, 64)}' +
                        '\n\n'.join(lang['game.text.debug']) % (VERSION['str'], x, y, z, rx, ry, mem, fps))
                self.label['top'].draw()
        else:
            # 初始化屏幕
            self.loading.draw()
            self.label['center'].document = decode_attributed('{color (255, 255, 255, 255)}{font_size 15}' +
                    lang['game.text.loading'])
            self.label['center'].draw()

    def draw_reticle(self):
        # 在屏幕中央画十字线
        if not self.is_init and not self.player['in_hud'] and self.exclusive:
            glColor3f(1.0, 1.0, 1.0)
            glLineWidth(3.0)
            self.reticle.draw(GL_LINES)
            glLineWidth(1.0)


def setup():
    # 基本的 OpenGL 设置
    glClearColor(0.5, 0.69, 1.0, 1)
    glEnable(GL_CULL_FACE)
    glEnable(GL_BLEND)
    glEnable(GL_LINE_SMOOTH)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    # 配置 OpenGL 的雾属性
    glEnable(GL_FOG)
    glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0.5, 0.69, 1.0, 1))
    glHint(GL_FOG_HINT, GL_DONT_CARE)
    glFogi(GL_FOG_MODE, GL_LINEAR)
    glFogf(GL_FOG_START, 30.0)
    glFogf(GL_FOG_END, 80.0)

