import math
import os
import random
import sys
import time

import Minecraft.saver as saver
from Minecraft.source import block, path, player, lang, settings
from Minecraft.gui.bag import Bag
from Minecraft.gui.dialogue import Dialogue
from Minecraft.gui.hotbar import HotBar
from Minecraft.gui.hud.heart import Heart
from Minecraft.gui.hud.hunger import Hunger
from Minecraft.gui.loading import Loading
from Minecraft.world.world import World
from Minecraft.utils.utils import *

try:
    import js2py as js
    import js2py.base as base
except ModuleNotFoundError:
    log_err("module 'Js2Py' not found, run `pip install js2py` to install, exit")
    exit(1)

try:
    import opensimplex
except ModuleNotFoundError:
    log_err("module 'opensimplex' not found. run `pip install opensimplex` to install, exit")
    exit(1)

try:
    import pyglet
    from pyglet import image
    from pyglet.gl import *
    from pyglet.shapes import Rectangle
    from pyglet.text import decode_attributed
    from pyglet.window import key, mouse
except:
    log_err("module 'pyglet' not found. run `pip install pyglet` to install, exit")
    exit(1)

try:
    import pyshaders
except:
    log_err("module 'pyshaders' not found. run `pip install pyshaders` to install, exit")
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
        # 玩家视角
        self.player['fovy'] = 65
        # 拓展功能
        self.ext = {}
        self.ext['debug'] = False
        self.ext['enable'] = False
        self.ext['position'] = False
        self.ext['running'] = False
        # rotation = (水平角 x, 俯仰角 y)
        self.rotation = (0, 0)
        # 玩家所处的区域
        self.sector = None
        # 这个十字在屏幕中央
        self.reticle = None
        # y 轴的加速度
        self.dy = 0
        # 玩家可以放置的方块, 使用数字键切换
        self.inventory = ['grass', 'dirt', 'sand', 'stone', 'log', 'leaf', 'brick', 'plank', 'craft_table']
        # 玩家手持的方块
        self.block = 0
        # 数字键列表
        self.num_keys = [
            key._1, key._2, key._3, key._4, key._5,
            key._6, key._7, key._8, key._9, key._0]
        # 这个标签在画布的上方显示
        self.label = {}
        self.label['top'] = pyglet.text.DocumentLabel(decode_attributed(''),
            x=0, y=self.height - 30,width=self.width // 2, multiline=True, anchor_x='left', anchor_y='center')
        self.is_init = True
        # 这个标签在画布正中偏上显示
        self.label['center'] = pyglet.text.DocumentLabel(decode_attributed(''),
            x=self.width // 2, y=self.height // 2 + 50, anchor_x='center', anchor_y='center')
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
        log_info('welcome %s' % player['name'])

    def __sizeof__(self):
        # 返回游戏所用的内存(有出入)
        if not self.is_init:
            total = 0
            for obj in dir(self.world):
                total += sys.getsizeof(getattr(self.world, obj))
            else:
                for obj in dir(self):
                    total += sys.getsizeof(getattr(self, obj))
                else:
                    return total
        else:
            return 0

    def check_die(self, dt):
        """
        这个函数被 pyglet 计时器反复调用

        :param: dt 距上次调用的时间
        """
        if not self.player['die']:
            if self.player['position'][1] < -2:
                self.set_exclusive_mouse(False)
                self.player['die_reason'] = lang['game.text.die.fall_into_void'] % player['name']
                log_info('%s die: %s' % (player['name'], self.player['die_reason']))
                self.player['die'] = True
                self.dialogue.add_dialogue(self.player['die_reason'])
            elif self.player['position'][1] > 512:
                self.set_exclusive_mouse(False)
                self.player['die_reason'] = lang['game.text.die.no_oxygen'] % player['name']
                log_info('%s die: %s' % (player['name'], self.player['die_reason']))
                self.player['die'] = True
                self.dialogue.add_dialogue(self.player['die_reason'])

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
        
    def save(self, dt):
        """
        这个函数被 pyglet 计时器反复调用

        :param: dt 距上次调用的时间
        """
        saver.save_block(self.name, self.world.change)
        saver.save_player(self.name, self.player['position'], self.player['respawn_position'], self.block)

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
        if (x, y, z) in self.world.world:
            return self.world.world[(x, y, z)]
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
        elif self.world.world[(x, y, z)] != block:
            return False
        else:
            return True
        
    def set_name(self, name):
        # 设置游戏存档名
        self.name = name
        self.world = World(name)
        # 读取玩家位置和背包
        data = saver.load_player(self.name)
        self.player['position'] = data['position']
        self.player['respawn_position'] = data['respawn']
        self.block = data['now_block']
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

    def get_sight_vector(self):
        # 返回玩家的视线方向
        x, y = self.rotation
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
        if any(self.player['strafe']):
            x, y = self.rotation
            strafe = math.degrees(math.atan2(*self.player['strafe']))
            y_angle = math.radians(y)
            x_angle = math.radians(x + strafe)
            if self.player['flying']:
                pass
            else:
                dy = 0.0
                dx = math.cos(x_angle)
                dz = math.sin(x_angle)
        elif self.player['flying'] and not self.dy == 0:
            dx = 0.0
            dy = self.dy
            dz = 0.0
        else:
            dy = 0.0
            dx = 0.0
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
            self.world.change_sectors(self.sector, sector)
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
            for position in [exist for exist in area if exist in self.world.world]:
                block = self.world.world[position]
                if block == 'dirt' and random.randint(0, 10) == 10:
                    for x, z in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        if (pos := (position[0] + x, position[1], position[2] + z)) in self.world.world:
                            if self.world.world[pos] == 'grass' and (pos[0], pos[1] + 1, pos[2]) not in self.world.world:
                                self.world.add_block(position, 'grass')
                elif block == 'grass':
                    if (position[0], position[1] + 1, position[2]) in self.world.world:
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
        d = dt * speed # 这一个游戏刻玩家经过的距离
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
                    if tuple(op) not in self.world.world:
                        continue
                    p[i] -= (d - pad) * face[i]
                    if face == (0, -1, 0) or face == (0, 1, 0):
                        self.dy = 0
                    break
        else:
            return tuple(p)

    def on_close(self):
        # 当玩家关闭窗口时调用
        saver.save_window(self.width, self.height)
        pyglet.app.exit()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        当玩家按下鼠标按键时调用
  
        :param: x, y 鼠标点击时的坐标, 如果被捕获的话总是在屏幕中央
        :param: button 哪个按键被按下: 1 = 左键, 4 = 右键
        :param: modifiers 表示单击鼠标按钮时按下的任何修改键的数字
        """
        if self.exclusive:
            vector = self.get_sight_vector()
            block, previous = self.world.hit_test(self.player['position'], vector)
            if block:
                texture = self.world.world[block]
            else:
                texture = None
            if (button == mouse.RIGHT) or ((button == mouse.LEFT) and (modifiers & key.MOD_CTRL)):
                # 在 Mac OS X 中, Ctrl + 左键 = 右键
                if not self.player['die'] and not self.player['in_hud']:
                    if texture == 'craft_table' and (not self.player['stealing']):
                        self.set_exclusive_mouse(False)
                    elif previous:
                        self.world.add_block(previous, self.inventory[self.block])
                        if self.has_script:
                            try:
                                if hasattr(self.js, 'onBuild'):
                                    self.js.onBuild(previous[0], previous[1], previous[2], self.inventory[self.block])
                            except Exception as err:
                                log_warn('script.js: onBuild: %s' % str(err))
            elif button == pyglet.window.mouse.LEFT and block:
                if texture != 'bedrock' and not self.player['die'] and not self.player['in_hud']:
                    self.world.remove_block(block)
                    if self.has_script:
                        try:
                            if hasattr(self.js, 'onDestroy'):
                                self.js.onDestroy(previous[0], previous[1], previous[2], texture)
                        except Exception as err:
                            log_warn('script.js: onDestroy: %s' % str(err))
            elif button == pyglet.window.mouse.MIDDLE and block:
                self.block = texture
        elif not self.player['die'] and not self.player['in_hud']:
            self.set_exclusive_mouse(True)

    def on_mouse_motion(self, x, y, dx, dy):
        """
        当玩家移动鼠标时调用

        :param: x, y 鼠标点击时的坐标, 如果被捕获的话它们总是在屏幕中央
        :param: dx, dy 鼠标移动的距离
        """
        if self.exclusive and not self.player['die']:
            m = 0.15
            x, y = self.rotation
            x, y = x + dx * m, y + dy * m
            y = max(-90, min(90, y))
            self.rotation = (x, y)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        """
        当鼠标滚轮滚动时调用

        :param: scroll_x, scroll_y 鼠标滚轮滚动(scroll_y 为1时向上, 为-1时向下)
        """
        index = self.block + scroll_y
        if index > len(self.inventory) - 1:
            self.block = 0
        elif index < 0:
            self.block = len(self.inventory) - 1
        else:
            self.block = index
        log_info('mouse scroll: %d of %d' % (self.block, len(self.inventory) - 1))
        self.hud['hotbar'].set_index(index)

    def on_key_press(self, symbol, modifiers):
        """
        当玩家按下一个按键时调用

        :param: symbol 按下的键
        :param: modifiers 同时按下的修饰键
        """
        if symbol == key.W:
            self.player['strafe'][0] -= 1
        elif symbol == key.S:
            self.player['strafe'][0] += 1
        elif symbol == key.A:
            self.player['strafe'][1] -= 1
        elif symbol == key.D:
            if self.ext['enable']:
                self.ext['debug'] = not self.ext['debug']
                self.ext['position'] = False
            else:
                self.player['strafe'][1] += 1
        elif symbol == key.E:
            if not self.player['die']:
                self.set_exclusive_mouse(self.player['show_bag'])
                self.player['in_hud'] = not self.player['in_hud']
                self.player['show_bag'] = not self.player['show_bag']
        elif symbol == key.X:
            if self.player['fovy'] == 65:
                self.player['fovy'] = 20
            else:
                self.player['fovy'] = 65
        elif symbol == key.P:
            if self.ext['enable']:
                self.ext['position'] = not self.ext['position']
                self.ext['debug'] = False
        elif symbol == key.R:
            if self.ext['enable']:
                self.ext['running'] = not self.ext['running']
                self.ext['open'] = False
                log_info('%s(id: %s) extra function running: %s' % (player['name'],
                    player['id'], self.ext['running']))
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
            pyglet.image.get_buffer_manager().get_color_buffer().save(os.path.join(
                path['screenshot'], time.strftime('%Y-%m-%d %H:%M:%S screenshot.png')))
            self.dialogue.add_dialogue(time.strftime('screenshot saved in: screenshot/%Y-%m-%d %H:%M:%S screenshot.png'))
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
        self.label['top'].y = self.height - 30
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
        gluPerspective(self.player['fovy'], width / float(height), 0.1, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x, y = self.rotation
        glRotatef(x, 0, 1, 0)
        glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))
        x, y, z = self.player['position']
        glTranslatef(-x, -y, -z)

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
                self.draw_reticle()
                if self.player['in_hud'] and self.player['show_bag']:
                    self.full_screen.color = (0, 0, 0)
                    self.full_screen.opacity = 100
                    self.full_screen.draw()
                    self.hud['bag'].draw()
            elif self.player['die']:
                self.full_screen.color = (200, 0, 0)
                self.full_screen.opacity = 100
                self.full_screen.draw()
        self.set_2d()
        if not self.player['hide_hud']:
            self.draw_label()
        if self.is_init:
            self.set_minimum_size(800, 600)
            self.world.init_world()
            if self.has_script:
                try:
                    if hasattr(self.js, 'onInit'):
                        self.js.onInit()
                except Exception as err:
                    log_warn('script.js: onInit: %s' % str(err))
            self.init_player()
            self.set_exclusive_mouse(True)
            self.is_init = False

    def draw_focused_block(self):
        # 在十字线选中的方块绘制黑边
        vector = self.get_sight_vector()
        block = self.world.hit_test(self.player['position'], vector)[0]
        if block:
            x, y, z = block
            vertex_data = cube_vertices(x, y, z, 0.5001)
            glColor4f(0.0, 0.0, 0.0, 0.9)
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
            elif self.ext['position']:
                # 在屏幕左上角绘制标签
                x, y, z = self.player['position']
                self.label['top'].document = decode_attributed('{color (255, 255, 255, 255)}{background_color (0, 0, 0, 64)}' +
                        lang['game.text.position'] % (x, y, z, pyglet.clock.get_fps()))
                self.label['top'].draw()
            elif self.ext['debug']:
                x, y, z = self.player['position']
                rx, ry = self.rotation
                mem = sys.getsizeof(self)
                self.label['top'].y = self.height - 60
                self.label['top'].document = decode_attributed('{color (255, 255, 255, 255)}{background_color (0, 0, 0, 64)}' +
                        '\n\n'.join(lang['game.text.debug']) % (x, y, z, 0.0, ry, mem, pyglet.clock.get_fps()))
                self.label['top'].draw()
        else:
            # 初始化屏幕
            self.loading.draw()
            self.label['center'].document = decode_attributed('{color (255, 255, 255, 255)}{font_size 15}' +
                    lang['game.text.loading'])
            self.label['center'].draw()

    def draw_reticle(self):
        # 在屏幕中央画十字线
        if not self.is_init and not self.player['in_hud']:
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

