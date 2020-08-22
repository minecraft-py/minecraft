# Minecraft 主程序

import json
import math
import os
import random
import time
from collections import deque

import Minecraft.saver as saver
from Minecraft.source import block, sound, path

try:
    from noise import snoise2 as noise2
except ModuleNotFoundError:
    print("[err] Module 'noise' not found. run `pip install noise` to install, exit")
    exit(1)

try:
    import pyglet
    from pyglet import image
    from pyglet.gl import *
    from pyglet.graphics import TextureGroup
    from pyglet.window import key, mouse
except:
    print("[err] Module 'pyglet' not found. run `pip install pyglet` to install, exit")
    exit(1)

TICKS_PER_SEC = 20
SECTOR_SIZE = 16

MAX_SIZE = 64

STEALING_SPEED = 3
WALKING_SPEED = 5
RUNNING_SPEED = 8
FLYING_SPEED = 10

GRAVITY = 20.0
MAX_JUMP_HEIGHT = 1.0 # 大约是每个方块的高度
# 获得跳跃的高度, 首先计算公式:
#    v_t = v_0 + a * t
# for the time at which you achieve maximum height, where a is the acceleration
# due to gravity and v_t = 0. This gives:
#    t = - v_0 / a
# Use t and the desired MAX_JUMP_HEIGHT to solve for v_0 (jump speed) in
#    s = s_0 + v_0 * t + (a * t ** 2) / 2
JUMP_SPEED = math.sqrt(2 * GRAVITY * MAX_JUMP_HEIGHT)
TERMINAL_VELOCITY = 50

PLAYER_HEIGHT = 2

def cube_vertices(x, y, z, n):
    # 返回在 x, y, z 坐标的方形顶点
    return [
        x-n,y+n,z-n, x-n,y+n,z+n, x+n,y+n,z+n, x+n,y+n,z-n,  # 顶部
        x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  # 底部
        x-n,y-n,z-n, x-n,y-n,z+n, x-n,y+n,z+n, x-n,y+n,z-n,  # 左边
        x+n,y-n,z+n, x+n,y-n,z-n, x+n,y+n,z-n, x+n,y+n,z+n,  # 右边
        x-n,y-n,z+n, x+n,y-n,z+n, x+n,y+n,z+n, x-n,y+n,z+n,  # 前面
        x+n,y-n,z-n, x-n,y-n,z-n, x-n,y+n,z-n, x+n,y+n,z-n,  # 后面
    ]

FACES = [
    ( 0, 1, 0),
    ( 0,-1, 0),
    (-1, 0, 0),
    ( 1, 0, 0),
    ( 0, 0, 1),
    ( 0, 0,-1),
]

def normalize(position):
    """ Accepts `position` of arbitrary precision and returns the block
    containing that position.

    Parameters
    ----------
    position : tuple of len 3

    Returns
    -------
    block_position : tuple of ints of len 3

    """
    x, y, z = position
    x, y, z = (int(round(x)), int(round(y)), int(round(z)))
    return (x, y, z)

def sectorize(position):
    """ Returns a tuple representing the sector for the given `position`.

    Parameters
    ----------
    position : tuple of len 3

    Returns
    -------
    sector : tuple of len 3

    """
    x, y, z = normalize(position)
    x, y, z = x // SECTOR_SIZE, y // SECTOR_SIZE, z // SECTOR_SIZE
    return (x, 0, z)


class Model(object):

    def __init__(self, name):
        # Batch 是用于批处理渲染的顶点列表的集合
        self.batch = pyglet.graphics.Batch()
        # A TextureGroup manages an OpenGL texture.
        self.group = TextureGroup(image.load(os.path.join(path['texture'], 'block.png')).get_texture())
        # 存档名
        self.name = name
        # A mapping from position to the texture of the block at that position.
        # This defines all the blocks that are currently in the world.
        self.world = {}
        # Same mapping as `world` but only contains blocks that are shown.
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
        # 放置所有方块以初始化世界
        print('[info] init world')
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
        print('[info] load block')
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
            # 建筑限制为基岩以上, 256格以下
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
        self._shown[position] = self.batch.add(24, GL_QUADS, self.group,
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
        self.stealing = False
        self.flying = False
        self.running = False
        # Strafing is moving lateral to the direction you are facing,
        # e.g. moving to the left or right while continuing to face forward.
        #
        # First element is -1 when moving forward, 1 when moving back, and 0
        # otherwise. The second element is -1 when moving left, 1 when moving
        # right, and 0 otherwise.
        self.strafe = [0, 0]
        # 玩家在世界中的位置 (x, y, z)
        self.position = (0, 4, 0)
        # First element is rotation of the player in the x-z plane (ground
        # plane) measured from the z-axis down. The second is the rotation
        # angle from the ground plane up. Rotation is in degrees.
        #
        # The vertical plane rotation ranges from -90 (looking straight down) to
        # 90 (looking straight up). The horizontal rotation range is unbounded.
        self.rotation = (0, 0)
        # Which sector the player is currently in.
        self.sector = None
        # The crosshairs at the center of the screen.
        self.reticle = None
        # Velocity in the y (upward) direction.
        self.dy = 0
        # 玩家可以放置的方块, 使用数字键切换
        self.inventory = ['grass', 'dirt', 'sand', 'stone', 'log', 'leaf', 'brick', 'plank', 'craft_table']
        # 玩家手持的方块
        self.block = self.inventory[0]
        # 数字键列表
        self.num_keys = [
            key._1, key._2, key._3, key._4, key._5,
            key._6, key._7, key._8, key._9, key._0]
        # 这个标签在画布的上方显示
        self.label = pyglet.text.Label('', font_name='Arial', font_size=18,
            x=0, y=self.height - 15, anchor_x='left', anchor_y='center',
            color=(0, 0, 0, 255))
        self.is_init =True
        self.loading_label = pyglet.text.Label('', font_name='Arial', font_size=20,
            x=self.width // 2, y=self.height // 2 + 20, anchor_x='center', anchor_y='center',
            color=(255, 255, 255, 200))
        self.loading_image = image.load(os.path.join(path['texture'], 'loading.png'))
        self.loading_image.height = self.height
        self.loading_image.width = self.width
        # 将 self.upgrade() 方法每 1.0 / TICKS_PER_SEC 调用一次, 它是游戏的主事件循环
        pyglet.clock.schedule_interval(self.update, 1.0 / TICKS_PER_SEC)
        # 每10秒更新一次方块数据
        pyglet.clock.schedule_interval(self.update_status, 10.0)
        # 每60秒保存一次进度
        pyglet.clock.schedule_interval(self.save, 30.0)
        # 读取玩家位置和背包
        self.position, self.block = saver.load_player('demo')

    def save(self, dt):
        """
        这个函数被 pyglet 计时器反复调用

        @param dt 距上次调用的时间
        """
        print('[info] save changes')
        saver.save_block(self.name, self.model.change)
        saver.save_player(self.name, self.position, self.block)

    def set_exclusive_mouse(self, exclusive):
        # 如果 exclusive 为 True, 窗口会捕获鼠标. 否则忽略之
        super(Window, self).set_exclusive_mouse(exclusive)
        self.exclusive = exclusive

    def set_name(self, name):
        # 设置游戏存档名
        self.name = name
        self.model = Model(name)

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
        if any(self.strafe):
            x, y = self.rotation
            strafe = math.degrees(math.atan2(*self.strafe))
            y_angle = math.radians(y)
            x_angle = math.radians(x + strafe)
            if self.flying:
                m = math.cos(y_angle)
                dy = math.sin(y_angle)
                if self.strafe[1]:
                    # 向左或右移动
                    dy = 0.0
                    m = 1
                if self.strafe[0] > 0:
                    # 向后移动
                    dy *= -1
                # When you are flying up or down, you have less left and right
                # motion.
                dx = math.cos(x_angle) * m
                dz = math.sin(x_angle) * m
            else:
                dy = 0.0
                dx = math.cos(x_angle)
                dz = math.sin(x_angle)
        elif self.flying and not self.dy == 0:
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
        sector = sectorize(self.position)
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
        print('[info] update status')
        area = []
        for x in range(int(self.position[0]) - 16, int(self.position[0]) + 17):
            for y in range(int(self.position[1]) - 16, int(self.position[1]) + 17):
                for z in range(int(self.position[2]) - 16, int(self.position[2]) + 17):
                    # 以玩家为中心的 32*32*32 范围
                    area.append((x, y, z))
        else:
            for position in [exist for exist in area if exist in self.model.world]:
                block = self.model.world[position]
                if block == 'dirt' and random.randint(1, 10) == 10:
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
        if self.flying:
            speed = FLYING_SPEED
        elif self.running:
            speed = RUNNING_SPEED
        elif self.stealing:
            speed = STEALING_SPEED
        else:
            speed = WALKING_SPEED
        d = dt * speed # distance covered this tick.
        dx, dy, dz = self.get_motion_vector()
        # New position in space, before accounting for gravity.
        dx, dy, dz = dx * d, dy * d, dz * d
        # 重力
        if not self.flying:
            # Update your vertical speed: if you are falling, speed up until you
            # hit terminal velocity; if you are jumping, slow down until you
            # start falling.
            self.dy -= dt * GRAVITY
            self.dy = max(self.dy, -TERMINAL_VELOCITY)
            dy += self.dy * dt
        # collisions
        x, y, z = self.position
        x, y, z = self.collide((x + dx, y + dy, z + dz), PLAYER_HEIGHT)
        self.position = (x, y, z)

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
            block, previous = self.model.hit_test(self.position, vector)
            if block:
                texture = self.model.world[block]
            else:
                texture = None
            if (button == mouse.RIGHT) or ((button == mouse.LEFT) and (modifiers & key.MOD_CTRL)):
                # 在 Mac OS X 中, Ctrl + 左键 = 右键
                if texture == 'craft_table' and (not self.stealing):
                    self.set_exclusive_mouse(False)
                elif previous:
                    self.model.add_block(previous, self.block)
            elif button == pyglet.window.mouse.LEFT and block:
                if texture != 'bedrock':
                    self.model.remove_block(block)
        else:
            self.set_exclusive_mouse(True)

    def on_mouse_motion(self, x, y, dx, dy):
        """
        当玩家移动鼠标时调用

        @param x, y 鼠标点击时的坐标, 如果被捕获的话总是在屏幕中央
        @param dx, dy 鼠标移动的距离
        """
        if self.exclusive:
            m = 0.15
            x, y = self.rotation
            x, y = x + dx * m, y + dy * m
            y = max(-90, min(90, y))
            self.rotation = (x, y)

    def on_key_press(self, symbol, modifiers):
        """
        当玩家按下一个按键时调用

        @param symbol 按下的键
        @param modifiers 同时按下的修饰键
        """
        if symbol == key.W:
            self.strafe[0] -= 1
        elif symbol == key.S:
            self.strafe[0] += 1
        elif symbol == key.A:
            self.strafe[1] -= 1
        elif symbol == key.D:
            self.strafe[1] += 1
        elif symbol == key.E:
            self.set_exclusive_mouse(False)
        elif symbol == key.SPACE:
            if self.flying:
                self.dy = 0.5 * JUMP_SPEED
            elif self.dy == 0:
                self.dy = JUMP_SPEED
        elif symbol == key.ESCAPE:
            self.save(0)
            self.set_exclusive_mouse(False)
        elif symbol == key.TAB:
            self.flying = not self.flying
        elif symbol == key.LSHIFT:
            if self.flying:
                self.dy = -0.5 * JUMP_SPEED
            else:
                self.stealing = True
        elif symbol == key.LCTRL:
            if not self.flying:
                self.running = True
        elif symbol in self.num_keys:
            index = (symbol - self.num_keys[0]) % len(self.inventory)
            self.block = self.inventory[index]
        elif symbol == key.F2:
            pyglet.image.get_buffer_manager().get_color_buffer().save(time.strftime('%Y-%m-%d %H:%M:%S screenshot.png'))
            print("[info] screenshot saved in: %s" % time.strftime('%Y-%m-%d %H:%M:%S screenshot.png'))

    def on_key_release(self, symbol, modifiers):
        """
        当玩家释放一个按键时调用
        
        @param symbol 按下的键
        """
        if symbol == key.W:
            self.strafe[0] += 1
        elif symbol == key.S:
            self.strafe[0] -= 1
        elif symbol == key.A:
            self.strafe[1] += 1
        elif symbol == key.D:
            self.strafe[1] -= 1
        elif symbol == key.LSHIFT:
            self.stealing = False
        elif symbol == key.LCTRL:
            self.running = False

    def on_resize(self, width, height):
        # 当窗口被调整到一个新的宽度和高度时调用
        # 标签
        print('[info] resize to %dx%d' % (self.width, self.height))
        self.label.x = 0
        self.label.y = self.height - 15
        # 窗口中央的十字线
        if self.reticle:
            self.reticle.delete()
        x, y = self.width // 2, self.height // 2
        n = 10
        self.reticle = pyglet.graphics.vertex_list(4,
            ('v2i', (x - n, y, x + n, y, x, y - n, x, y + n))
        )

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
        x, y, z = self.position
        glTranslatef(-x, -y, -z)

    def on_draw(self):
        # 当 pyglet 在画布上绘图时调用
        self.clear()
        if not self.is_init:
            self.set_3d()
            glColor3d(1, 1, 1)
            self.model.batch.draw()
            self.draw_focused_block()
            self.set_2d()
            self.draw_reticle()
        self.set_2d()
        self.draw_label()
        if self.is_init:
            self.model.init_world()
            self.loading_label.delete()
            self.is_init = False

    def draw_focused_block(self):
        # 在十字线选中的方块绘制黑边
        vector = self.get_sight_vector()
        block = self.model.hit_test(self.position, vector)[0]
        if block:
            x, y, z = block
            vertex_data = cube_vertices(x, y, z, 0.51)
            glColor3d(0, 0, 0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            pyglet.graphics.draw(24, GL_QUADS, ('v3f/static', vertex_data))
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def draw_label(self):
        # 在屏幕左上方绘制标签
        if not self.is_init:
            x, y, z = self.position
            self.label.text = '(%.1f %.1f %.1f) %-4d' % (
                x, y, z, pyglet.clock.get_fps())
            self.label.draw()
        else:
            self.loading_image.blit(0, 0)
            self.loading_label.text = 'Loading...'
            self.loading_label.draw()

    def draw_reticle(self):
        # 在屏幕中央画十字线
        if not self.is_init:
            glColor3d(0, 0, 0)
            self.reticle.draw(GL_LINES)


def setup_fog():
    # 配置 OpenGL 的雾属性
    print('[info] setup fog')
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
    print('[info] setup light')
    # 启用双面光照
    glLightModeli(GL_LIGHT_MODEL_TWO_SIDE , GL_TRUE)
    # 光源衰减
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION ,1.0)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION ,0.0)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION ,0.0)
    # 设置0号光源
    glLightfv(GL_LIGHT0, GL_DIFFUSE , (GLfloat * 4)(1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (GLfloat * 4)(1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_POSITION, (GLfloat * 4)(0, 1, 0, 1))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)

def setup():
    # 基本的 OpenGL 设置
    print('[info] setup')
    # 设置背景颜色. 比如在 RGBA 模式下的天空
    glClearColor(0.5, 0.69, 1.0, 1)
    # Enable culling (not rendering) of back-facing facets -- facets that aren't
    # visible to you.
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

