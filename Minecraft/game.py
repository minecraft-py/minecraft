# Minecraft 主程序

from collections import deque
import json
import math
import os
import random
import sys
import time

try:
    import js2py as js
    import js2py.base as base
except ModuleNotFoundError:
    log_err("Module 'Js2Py' not found, run `pip install js2py` to install, exit")
    exit(1)

try:
    from noise import snoise2 as noise2
except ModuleNotFoundError:
    log_err("Module 'noise' not found. run `pip install noise` to install, exit")
    exit(1)

try:
    import pyglet
    from pyglet import image
    from pyglet.gl import *
    from pyglet.graphics import TextureGroup
    from pyglet.shapes import Rectangle
    from pyglet.sprite import Sprite
    from pyglet.text import decode_attributed
    from pyglet.window import key, mouse
except:
    log_err("Module 'pyglet' not found. run `pip install pyglet` to install, exit")
    exit(1)

try:
    import pyshaders
except:
    log_err("Module 'pyshaders' not found. run `pip install pyshaders` to install, exit")
    exit(1)

import Minecraft.saver as saver
from Minecraft.source import block, sound, path, player, lang, settings
from Minecraft.gui.bag import Bag
from Minecraft.gui.dialogue import Dialogue
from Minecraft.gui.hotbar import HotBar
from Minecraft.gui.hud.heart import Heart
from Minecraft.gui.hud.hunger import Hunger
from Minecraft.utils.utils import *


class Model(object):

    def __init__(self, name):
        # Batch 是用于批处理渲染的顶点列表的集合
        self.batch3d = pyglet.graphics.Batch()
        # 为了分开绘制3D物体和2D的 HUD, 我们需要两个 Batch
        self.batch2d = pyglet.graphics.Batch()
        # 纹理的集合
        self.group = TextureGroup(image.load(os.path.join(path['texture'], 'block.png')).get_texture())
        # 存档名
        self.name = name
        # world 存储着世界上所有的方块
        self.world = {}
        # 类似于 world, 但它只存储要显示的方块
        self.shown = {}
        # Mapping from position to a pyglet `VertextList` for all shown blocks.
        self._shown = {}
        # 记录玩家改变的方块
        self.change = {}
        # Mapping from sector to a list of positions inside that sector.
        self.sectors = {}
        # Simple function queue implementation. The queue is populated with
        # _show_block() and _hide_block() calls
        self.queue = deque()

    def init_world(self):
        # 放置所有方块以初始化世界, 非常耗时
        log_info('init world')
        for x in range(-MAX_SIZE, MAX_SIZE + 1):
            for z in range(-MAX_SIZE, MAX_SIZE + 1):
                self.add_block((x, 0, z), 'bedrock', record=False)
        for x in range(-MAX_SIZE, MAX_SIZE + 1):
            for y in range(1, 3):
                for z in range(-MAX_SIZE, MAX_SIZE + 1):
                    self.add_block((x, y, z), 'dirt', record=False)
        for x in range(-MAX_SIZE, MAX_SIZE + 1):
            for z in range(-MAX_SIZE, MAX_SIZE + 1):
                self.add_block((x, y, z), 'grass', record=False)
        log_info('load block')
        saver.load_block(self.name, self.add_block, self.remove_block)

    def hit_test(self, position, vector, max_distance=8):
        """
        从当前位置开始视线搜索, 如果有任何方块与之相交, 返回之.
        如果没有找到, 返回 (None, None)

        @param position 长度为3的元组, 当前位置
        @param vector 长度为3的元组, 视线向量
        @param max_distance 在多少方块的范围内搜索
        """
        m = 8
        x, y, z = position
        dx, dy, dz = vector
        previous = None
        for _ in range(max_distance * m):
            key = normalize((x, y, z))
            if key != previous and key in self.world:
                return key, previous
            previous = key
            x, y, z = x + dx / m, y + dy / m, z + dz / m
        else:
            return None, None

    def exposed(self, position):
        # 如果 position 所有的六个面旁边都有方块, 返回 False. 否则返回 True
        x, y, z = position
        for dx, dy, dz in FACES:
            if (x + dx, y + dy, z + dz) not in self.world:
                return True
        else:
            return False

    def add_block(self, position, texture, immediate=True, record=True):
        """
        在 position 处添加一个纹理为 texture 的方块

        @param pssition 长度为3的元组, 要添加方块的位置
        @param texture 长度为3的列表, 纹理正方形的坐标, 使用 tex_coords() 创建
        @param immediate 是否立即绘制方块
        @param record 是否记录方块更改(在生成地形时不记录)
        """
        if position in self.world:
            self.remove_block(position, immediate, record=False)
        if 0 <= position[1] <= 256:
            # 建筑限制为基岩以上, 256格以下.
            if record == True:
                self.change[' '.join([str(i) for i in position])] = texture
            if texture in block:
                self.world[position] = texture
            else:
                # 将不存在的方块替换为 undefined
                self.world[position] = 'undefined'
            self.sectors.setdefault(sectorize(position), []).append(position)
            if immediate:
                if self.exposed(position):
                    self.show_block(position)
                self.check_neighbors(position)

    def remove_block(self, position, immediate=True, record=True):
        """
        在 position 处移除一个方块

        @param position 长度为3的元组, 要移除方块的位置
        @param immediate 是否要从画布上立即移除方块
        @param record 是否记录方块更改(在 add_block 破坏后放置时不记录)
        """
        if position in self.world:
            # 不加这个坐标是否存在于世界中的判断有极大概率会抛出异常
            del self.world[position]
            if record:
                self.change[' '.join([str(i) for i in position])] = 'air'
            self.sectors[sectorize(position)].remove(position)
            if immediate:
                if position in self.shown:
                    self.hide_block(position)
                self.check_neighbors(position)

    def check_neighbors(self, position):
        """
        检查 position 周围所有的方块, 确保它们的状态是最新的.
        这意味着将隐藏不可见的方块, 并显示可见的方块.
        通常在添加或删除方块时使用.
        """
        x, y, z = position
        for dx, dy, dz in FACES:
            key = (x + dx, y + dy, z + dz)
            if key not in self.world:
                continue
            if self.exposed(key):
                if key not in self.shown:
                    self.show_block(key)
            else:
                if key in self.shown:
                    self.hide_block(key)

    def show_block(self, position, immediate=True):
        """
        在 position 处显示方块, 这个方法假设方块在 add_block() 已经添加

        @param position 长度为3的元组, 要显示方块的位置
        @param immediate 是否立即显示方块
        """
        texture = block[self.world[position]]
        self.shown[position] = texture
        if immediate:
            self._show_block(position, texture)
        else:
            self._enqueue(self._show_block, position, texture)

    def _show_block(self, position, texture):
        """
        show_block() 方法的私有实现

        @param position 长度为3的元组, 要显示方块的位置
        @param texture 长度为3的列表, 纹理正方形的坐标, 使用 tex_coords() 创建
        """
        x, y, z = position
        vertex_data = cube_vertices(x, y, z, 0.5)
        texture_data = list(texture)
        # 创建向量列表
        # FIXME 应该使用 add_indexed() 来代替
        self._shown[position] = self.batch3d.add(24, GL_QUADS, self.group,
            ('v3f/static', vertex_data),
            ('t2f/static', texture_data))

    def hide_block(self, position, immediate=True):
        """
        隐藏在 position 处的方块, 它不移除方块

        @param position 长度为3的元组, 要隐藏方块的位置
        @param immediate 是否立即隐藏方块
        """
        self.shown.pop(position)
        if immediate:
            self._hide_block(position)
        else:
            self._enqueue(self._hide_block, position)

    def _hide_block(self, position):
        # hide_block() 方法的私有实现
        self._shown.pop(position).delete()

    def show_sector(self, sector):
        """ Ensure all blocks in the given sector that should be shown are
        drawn to the canvas.

        """
        for position in self.sectors.get(sector, []):
            if position not in self.shown and self.exposed(position):
                self.show_block(position, False)

    def hide_sector(self, sector):
        """ Ensure all blocks in the given sector that should be hidden are
        removed from the canvas.

        """
        for position in self.sectors.get(sector, []):
            if position in self.shown:
                self.hide_block(position, False)

    def change_sectors(self, before, after):
        """ Move from sector `before` to sector `after`. A sector is a
        contiguous x, y sub-region of world. Sectors are used to speed up
        world rendering.

        """
        before_set = set()
        after_set = set()
        pad = 4
        for dx in range(-pad, pad + 1):
            for dy in [0]:
                for dz in range(-pad, pad + 1):
                    if dx ** 2 + dy ** 2 + dz ** 2 > (pad + 1) ** 2:
                        continue
                    if before:
                        x, y, z = before
                        before_set.add((x + dx, y + dy, z + dz))
                    if after:
                        x, y, z = after
                        after_set.add((x + dx, y + dy, z + dz))
        else:
            show = after_set - before_set
            hide = before_set - after_set
            for sector in show:
                self.show_sector(sector)
            for sector in hide:
                self.hide_sector(sector)

    def _enqueue(self, func, *args):
        # 把 func 添加到内部的队列
        self.queue.append((func, args))

    def _dequeue(self):
        # 从内部队列顶部弹出函数并调用之
        func, args = self.queue.popleft()
        func(*args)

    def process_queue(self):
        """ Process the entire queue while taking periodic breaks. This allows
        the game loop to run smoothly. The queue contains calls to
        _show_block() and _hide_block() so this method should be called if
        add_block() or remove_block() was called with immediate=False

        """
        start = time.perf_counter()
        while self.queue and time.perf_counter() - start < 1.0 / TICKS_PER_SEC:
            self._dequeue()

    def process_entire_queue(self):
        """ Process the entire queue with no breaks.

        """
        while self.queue:
            self._dequeue()


class Window(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        # 窗口是否捕获鼠标
        self.exclusive = False
        # 玩家状态: 是否潜行, 是否飞行...
        self.player = {}
        self.player['stealing'] = False
        self.player['flying'] = False
        self.player['running'] = False
        self.player['die'] = False
        self.player['in_hud'] = False
        self.player['press_e'] = False
        # Strafing is moving lateral to the direction you are facing,
        # e.g. moving to the left or right while continuing to face forward.
        #
        # First element is -1 when moving forward, 1 when moving back, and 0
        # otherwise. The second element is -1 when moving left, 1 when moving
        # right, and 0 otherwise.
        self.player['strafe'] = [0, 0]
        # 玩家在世界中的位置 (x, y, z)
        self.player['position'] = (0, 4, 0)
        self.player['respawn_position'] = (0, 4, 0)
        # 拓展功能
        self.ext = {}
        self.ext['debug'] = False
        self.ext['open'] = False
        self.ext['position'] = False
        self.ext['running'] = False
        # First element is rotation of the player in the x-z plane (ground
        # plane) measured from the z-axis down. The second is the rotation
        # angle from the ground plane up. Rotation is in degrees.
        #
        # The vertical plane rotation ranges from -90 (looking straight down) to
        # 90 (looking straight up). The horizontal rotation range is unbounded.
        self.rotation = (0, 0)
        # Which sector the player is currently in.
        self.sector = None
        # 这个十字在屏幕中央
        self.reticle = None
        # Velocity in the y (upward) direction.
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
            x=0, y=self.height - 30, anchor_x='left', anchor_y='center')
        self.is_init =True
        # 这个标签在画布正中偏上显示
        self.label['center'] = pyglet.text.DocumentLabel(decode_attributed(''),
            x=self.width // 2, y=self.height // 2 + 50, anchor_x='center', anchor_y='center')
        # 这个标签在画布正中偏下显示
        self.label['actionbar'] = pyglet.text.DocumentLabel(decode_attributed(''),
                x=self.width // 2, y=self.height // 2 - 100, anchor_x='center', anchor_y='center')
        # 加载用图片
        self.loading_image = image.load(os.path.join(path['texture'], 'loading.png'))
        self.loading_image.height = self.height
        self.loading_image.width = self.width
        # 覆盖屏幕的矩形
        self.full_screen = Rectangle(0, 0, self.width, self.height)
        # 聊天区
        self.dialogue = Dialogue(self.width, self.height)
        # 将 self.upgrade() 方法每 1.0 / TICKS_PER_SEC 调用一次, 它是游戏的主事件循环
        pyglet.clock.schedule_interval(self.update, 1.0 / TICKS_PER_SEC)
        # 检测玩家是否应该死亡
        pyglet.clock.schedule_interval(self.check_die, 1.0 / TICKS_PER_SEC)
        # 每10秒更新一次方块数据
        pyglet.clock.schedule_interval(self.update_status, 10.0)
        # 每60秒保存一次进度
        pyglet.clock.schedule_interval(self.save, 30.0)
        log_info('welcome %s(id: %s)' % (player['name'], player['id']))

    def check_die(self, dt):
        """
        这个函数被 pyglet 计时器反复调用

        @param dt 距上次调用的时间
        """
        if not self.player['die']:
            if self.player['position'][1] < -2:
                self.set_exclusive_mouse(False)
                self.player['die_reason'] = lang['game.text.die.fall_into_void'] % player['name']
                log_info('%s(id: %s) die: %s' % (player['name'], player['id'], self.player['die_reason']))
                self.player['die'] = True
                self.dialogue.add_dialogue(self.player['die_reason'])
            elif self.player['position'][1] > 512:
                self.set_exclusive_mouse(False)
                self.player['die_reason'] = lang['game.text.die.no_oxygen'] % player['name']
                log_info('%s(id: %s) die: %s' % (player['name'], player['id'], self.player['die_reason']))
                self.player['die'] = True
                self.dialogue.add_dialogue(self.player['die_reason'])

    def init_player(self):
        # 初始化玩家
        self.hud = {}
        # E 键打开的背包
        self.hud['bag'] = Bag(self.width, self.height)
        # 生命值
        self.hud['heart'] = Heart(self.width, self.height, batch=self.model.batch2d)
        # 饥饿值
        self.hud['hunger'] = Hunger(self.width, self.height, batch=self.model.batch2d)
        # 工具栏
        self.hud['hotbar'] = HotBar(self.width, self.height)
        self.hud['hotbar'].set_index(self.width, self.block)
        
    def save(self, dt):
        """
        这个函数被 pyglet 计时器反复调用

        @param dt 距上次调用的时间
        """
        log_info('save changes')
        saver.save_block(self.name, self.model.change)
        saver.save_player(self.name, self.player['position'], self.player['respawn_position'], self.block)

    def set_exclusive_mouse(self, exclusive):
        # 如果 exclusive 为 True, 窗口会捕获鼠标. 否则忽略之
        super(Window, self).set_exclusive_mouse(exclusive)
        self.exclusive = exclusive

    def set_name(self, name):
        # 设置游戏存档名
        self.name = name
        self.model = Model(name)
        # 读取玩家位置和背包
        self.player['position'], self.player['respawn_position'], self.block = saver.load_player(self.name)
        # 读取 js 脚本
        if os.path.isfile(os.path.join(path['mcpypath'], 'save', name, 'script.js')):
            log_info('found script.js')
            self.has_script = True
            self.js = js.EvalJs()
            try:
                self.js.eval(open(os.path.join(path['mcpypath'], 'save', name, 'script.js')).read())
            except Exception as err:
                log_err('script.js: %s' % str(err))
                exit(1)
        else:
            self.has_script = False

    def get_sight_vector(self):
        """ Returns the current line of sight vector indicating the direction
        the player is looking.

        """
        x, y = self.rotation
        # y ranges from -90 to 90, or -pi/2 to pi/2, so m ranges from 0 to 1 and
        # is 1 when looking ahead parallel to the ground and 0 when looking
        # straight up or down.
        m = math.cos(math.radians(y))
        # dy ranges from -1 to 1 and is -1 when looking straight down and 1 when
        # looking straight up.
        dy = math.sin(math.radians(y))
        dx = math.cos(math.radians(x - 90)) * m
        dz = math.sin(math.radians(x - 90)) * m
        return (dx, dy, dz)

    def get_motion_vector(self):
        """ Returns the current motion vector indicating the velocity of the
        player.

        Returns
        -------
        vector : tuple of len 3
            Tuple containing the velocity in x, y, and z respectively.

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

        @param dt 距上次调用的时间
        """
        self.model.process_queue()
        self.dialogue.update()
        sector = sectorize(self.player['position'])
        if sector != self.sector:
            self.model.change_sectors(self.sector, sector)
            if self.sector is None:
                self.model.process_entire_queue()
            self.sector = sector
        m = 8
        dt = min(dt, 0.2)
        for _ in range(m):
            self._update(dt / m)

    def update_status(self, dt):
        # 这个函数定时改变世界状态
        log_info('update status')
        area = []
        for x in range(int(self.player['position'][0]) - 16, int(self.player['position'][0]) + 17):
            for y in range(int(self.player['position'][1]) - 2, int(self.player['position'][1]) + 3):
                for z in range(int(self.player['position'][2]) - 16, int(self.player['position'][2]) + 17):
                    # 以玩家为中心的 32*32*4 范围
                    area.append((x, y, z))
        else:
            for position in [exist for exist in area if exist in self.model.world]:
                block = self.model.world[position]
                if block == 'dirt' and random.randint(0, 10) == 10:
                    for x, z in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        if (pos := (position[0] + x, position[1], position[2] + z)) in self.model.world:
                            if self.model.world[pos] == 'grass' and (pos[0], pos[1] + 1, pos[2]) not in self.model.world:
                                self.model.add_block(position, 'grass')
                elif block == 'grass':
                    if (position[0], position[1] + 1, position[2]) in self.model.world:
                        self.model.add_block(position, 'dirt')
            
    def _update(self, dt):
        """ Private implementation of the `update()` method. This is where most
        of the motion logic lives, along with gravity and collision detection.

        Parameters
        ----------
        dt : float
            The change in time since the last call.

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
        d = dt * speed # distance covered this tick.
        dx, dy, dz = self.get_motion_vector()
        # New position in space, before accounting for gravity.
        dx, dy, dz = dx * d, dy * d, dz * d
        # 重力
        if not self.player['die']:
            if not self.player['flying']:
                # Update your vertical speed: if you are falling, speed up until you
                # hit terminal velocity; if you are jumping, slow down until you
                # start falling.
                self.dy -= dt * GRAVITY
                self.dy = max(self.dy, -TERMINAL_VELOCITY)
                dy += self.dy * dt
            if not self.player['in_hud']:
                # collisions
                x, y, z = self.player['position']
                x, y, z = self.collide((x + dx, y + dy, z + dz), PLAYER_HEIGHT)
                self.player['position'] = (x, y, z)

    def collide(self, position, height):
        """ Checks to see if the player at the given `position` and `height`
        is colliding with any blocks in the world.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position to check for collisions at.
        height : int or float
            The height of the player.

        Returns
        -------
        position : tuple of len 3
            The new position of the player taking into account collisions.

        """
        # How much overlap with a dimension of a surrounding block you need to
        # have to count as a collision. If 0, touching terrain at all counts as
        # a collision. If .49, you sink into the ground, as if walking through
        # tall grass. If >= .5, you'll fall through the ground.
        pad = 0.25
        p = list(position)
        np = normalize(position)
        for face in FACES:  # check all surrounding blocks
            for i in range(3):  # check each dimension independently
                if not face[i]:
                    continue
                # How much overlap you have with this dimension.
                d = (p[i] - np[i]) * face[i]
                if d < pad:
                    continue
                for dy in range(height):
                    op = list(np)
                    op[1] -= dy
                    op[i] += face[i]
                    if tuple(op) not in self.model.world:
                        continue
                    p[i] -= (d - pad) * face[i]
                    if face == (0, -1, 0) or face == (0, 1, 0):
                        # You are colliding with the ground or ceiling, so stop
                        # falling / rising.
                        self.dy = 0
                    break
        else:
            return tuple(p)

    def on_mouse_press(self, x, y, button, modifiers):
        """
        当玩家按下鼠标按键时调用
  
        @param x, y 鼠标点击时的坐标, 如果被捕获的话总是在屏幕中央
        @param button 哪个按键被按下: 1 = 左键, 4 = 右键
        @param modifiers 表示单击鼠标按钮时按下的任何修改键的数字
        """
        if self.exclusive:
            vector = self.get_sight_vector()
            block, previous = self.model.hit_test(self.player['position'], vector)
            if block:
                texture = self.model.world[block]
            else:
                texture = None
            if (button == mouse.RIGHT) or ((button == mouse.LEFT) and (modifiers & key.MOD_CTRL)):
                # 在 Mac OS X 中, Ctrl + 左键 = 右键
                if not self.player['die'] and not self.player['in_hud']:
                    if texture == 'craft_table' and (not self.player['stealing']):
                        self.set_exclusive_mouse(False)
                    elif previous:
                        self.model.add_block(previous, self.inventory[self.block])
            elif button == pyglet.window.mouse.LEFT and block:
                if texture != 'bedrock' and not self.player['die'] and not self.player['in_hud']:
                    self.model.remove_block(block)
            elif button == pyglet.window.mouse.MIDDLE and block:
                self.block = texture
        elif not self.player['die'] and not self.player['in_hud']:
            self.set_exclusive_mouse(True)

    def on_mouse_motion(self, x, y, dx, dy):
        """
        当玩家移动鼠标时调用

        @param x, y 鼠标点击时的坐标, 如果被捕获的话总是在屏幕中央
        @param dx, dy 鼠标移动的距离
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

        @param scroll_x, scroll_y 鼠标滚轮滚动(scroll_y 为1时向上, 为-1时向下)
        """
        index = self.block + scroll_y
        if index < 0:
            self.block = len(self.inventory) + index
        elif index > len(self.inventory) - 1:
            self.block = index - len(self.inventory) - 1
        else:
            self.block = index
        log_info('mouse scroll: %d of %d' % (self.block, len(self.inventory) - 1))
        self.hud['hotbar'].set_index(self.width, index)

    def on_key_press(self, symbol, modifiers):
        """
        当玩家按下一个按键时调用

        @param symbol 按下的键
        @param modifiers 同时按下的修饰键
        """
        if symbol == key.W:
            self.player['strafe'][0] -= 1
        elif symbol == key.S:
            self.player['strafe'][0] += 1
        elif symbol == key.A:
            self.player['strafe'][1] -= 1
        elif symbol == key.D:
            if self.ext['open']:
                self.ext['debug'] = not self.ext['debug']
                self.ext['position'] = False
                self.ext['open'] = False
                log_info('%s(id: %s) extra function debug: %s' % (player['name'],
                    player['id'], self.ext['debug']))
            else:
                self.player['strafe'][1] += 1
        elif symbol == key.E:
            if not self.player['die']:
                self.set_exclusive_mouse(False)
                self.player['in_hud'] = not self.player['in_hud']
                self.player['press_e'] = not self.player['press_e']
        elif symbol == key.P:
            if self.ext['open']:
                self.ext['position'] = not self.ext['position']
                self.ext['debug'] = False
                self.ext['open'] = False
                log_info('%s(id: %s) extra function position: %s' % (player['name'],
                    player['id'], self.ext['position']))
        elif symbol == key.R:
            if self.ext['open']:
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
            self.hud['hotbar'].set_index(self.width, self.block)
        elif symbol == key.F2:
            pyglet.image.get_buffer_manager().get_color_buffer().save(os.path.join(
                path['screenshot'], time.strftime('%Y-%m-%d %H:%M:%S screenshot.png')))
            log_info('screenshot saved in: %s' % time.strftime('$MCPYPATH/screenshot/%Y-%m-%d %H:%M:%S screenshot.png'))
        elif symbol == key.F3:
            self.ext['open'] = not self.ext['open']
        elif symbol == key.F11:
            self.set_fullscreen(not self.fullscreen)

    def on_key_release(self, symbol, modifiers):
        """
        当玩家释放一个按键时调用
        
        @param symbol 按下的键
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

    def on_resize(self, width, height):
        # 当窗口被调整到一个新的宽度和高度时调用
        # 标签
        log_info('resize to %dx%d' % (self.width, self.height))
        self.label['top'].x = 0
        self.label['top'].y = self.height - 30
        self.label['center'].x = self.width // 2
        self.label['center'].y = self.height // 2 + 50
        self.label['actionbar'].x = self.width // 2
        self.label['actionbar'].y = self.height // 2 - 100
        # 窗口中央的十字线
        if self.reticle:
            self.reticle.delete()
        x, y = self.width // 2, self.height // 2
        n = 10
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
        gluPerspective(65.0, width / float(height), 0.1, 60.0)
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
            self.model.batch3d.draw()
            self.draw_focused_block()
            self.set_2d()
            if not self.player['die']:
                self.model.batch2d.draw()
                self.hud['hotbar'].draw()
                self.draw_reticle()
                if self.player['in_hud'] and self.player['press_e']:
                    self.full_screen.color = (0, 0, 0)
                    self.full_screen.opacity = 100
                    self.full_screen.draw()
                    self.hud['bag'].draw()
            else:
                self.full_screen.color = (200, 0, 0)
                self.full_screen.opacity = 100
                self.full_screen.draw()
        self.set_2d()
        self.draw_label()
        if self.is_init:
            self.model.init_world()
            if self.has_script:
                try:
                    if hasattr(self.js, 'on_init'):
                        log_info('found script.js:on_init, run')
                        self.js.on_init()
                except Exception as err:
                    log_warn('script.js: on_init: %s' % str(err))
            self.init_player()
            self.set_exclusive_mouse(True)
            self.is_init = False

    def draw_focused_block(self):
        # 在十字线选中的方块绘制黑边
        vector = self.get_sight_vector()
        block = self.model.hit_test(self.player['position'], vector)[0]
        if block:
            x, y, z = block
            vertex_data = cube_vertices(x, y, z, 0.505)
            glColor3d(0, 0, 0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            pyglet.graphics.draw(24, GL_QUADS, ('v3f/static', vertex_data))
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def draw_label(self):
        if not self.is_init:
            if self.player['die']:
                # 玩家死亡
                self.dialogue.draw()
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
                self.dialogue.draw()
        else:
            # 初始化屏幕
            self.loading_image.blit(0, 0)
            self.label['center'].document = decode_attributed('{color (255, 255, 255, 255)}{font_size 15}' +
                    lang['game.text.loading'])
            self.label['center'].draw()

    def draw_reticle(self):
        # 在屏幕中央画十字线
        if not self.is_init:
            glColor3d(0, 0, 0)
            self.reticle.draw(GL_LINES)


def setup_fog():
    # 配置 OpenGL 的雾属性
    log_info('setup fog')
    # 启用雾
    glEnable(GL_FOG)
    # 设置雾的颜色
    glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0.5, 0.69, 1.0, 1))
    # 如果我们在渲染速度和质量之间没有取舍
    glHint(GL_FOG_HINT, GL_DONT_CARE)
    # 指定用于计算混合因子的公式
    glFogi(GL_FOG_MODE, GL_LINEAR)
    # 雾的终点和起点有多远. 起点和终点越近, 范围内的雾就越密集
    glFogf(GL_FOG_START, 30.0)
    glFogf(GL_FOG_END, 80.0)

def setup_light():
    # 设置 OpenGL 环境光
    log_info('setup light')
    # 启用双面光照
    glLightModeli(GL_LIGHT_MODEL_TWO_SIDE , GL_TRUE)
    # 光源衰减
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION ,1.0)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION ,0.0)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION ,0.0)
    # 设置0号光源
    glLightfv(GL_LIGHT0, GL_DIFFUSE , (GLfloat * 4)(1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (GLfloat * 4)(1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_POSITION, (GLfloat * 4)(0, 0, 0, -1))
    # 开灯
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)

def setup():
    # 基本的 OpenGL 设置
    log_info('setup')
    # 设置背景颜色. 比如在 RGBA 模式下的天空
    glClearColor(0.5, 0.69, 1.0, 1)
    # 启用面剔除
    glEnable(GL_CULL_FACE)
    # Set the texture minification/magnification function to GL_NEAREST (nearest
    # in Manhattan distance) to the specified texture coordinates. GL_NEAREST
    # "is generally faster than GL_LINEAR, but it can produce textured images
    # with sharper edges because the transition between texture elements is not
    # as smooth."
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    setup_fog()
    # setup_light()

