# Minecraft-in-python, a sandbox game
# Copyright (C) 2020-2023  Minecraft-in-python team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
from os import environ, path
from pathlib import Path
from typing import Tuple, Union

import pyglet

# 一个方块周围6个方块的相对坐标
FACES = [
    (0, 1, 0),
    (0, -1, 0),
    (1, 0, 0),
    (-1, 0, 0),
    (0, 0, 1),
    (0, 0, -1),
]

# 游戏版本信息
VERSION = {
    "major": 0,
    "minor": 0,
    "patch": 1,
    "str": "0.0.1",
    # 如果data是一个浮点数，那说明现在正处于开发版本
    "data": 1.5
}


def get_caller(full=False) -> str:
    """获取调用栈中倒数第三个函数所在的包名。

    调用栈：

    1. 函数1（调用了函数2）
    2. 函数2（调用了本函数）
    3. 本函数（返回函数1所在的包名）
    """
    name = sys._getframe().f_back.f_back.f_code.co_filename
    # 返回的不是文件系统路径而是一个对象则报错
    assert name[0] == "<", "caller's caller is not in a function"
    for p in sys.path:
        if name.startswith(p):
            p1, p2 = Path(p).parts, Path(name).parts
            if full:
                pkg_path = list(p2[len(p1):])
                pkg_path[-1] = pkg_path[-1][:-3]
                return ".".join(pkg_path)
            else:
                return p2[len(p1)]


def get_game() -> pyglet.window.Window:
    """获取GameWindow类的实例。

    根据程序算法，只能存在一个`minecraft.scene.GameWindow`对象。

    若直接导入模块运行该函数会引发异常。
    """
    for w in pyglet.canvas.get_display().get_windows():
        if str(w).startswith("GameWindow"):
            return w
    raise RuntimeError("no GameWindow found")


def get_size() -> Tuple[int, int]:
    """返回窗口大小。"""
    w = get_game()
    return w.width, w.height


def is_namespace(s: str) -> bool:
    """判断一个字符串是否是命名空间。

    命名空间应该满足`[顶层命名空间]:<子命名空间1>.<子命名空间2>...<子命名空间n>`。

    顶层命名空间可省略，默认为`minecraft`；子命名空间用`.`分隔。

    使用`str.partition()`检测命名空间是否合法。
    """
    l = s.partition(":")
    if s.partition(":")[1]:
        return l[0].isidentifier() and all([sub.isidentifier() for sub in l[2].split(".")])
    else:
        return all([sub.isidentifier() for sub in l[0].split(".")])


def mdist(p: Union[int, float], q: Union[int, float]) -> Union[int, float]:
    """计算同一维度内的点p和q之间的距离。"""
    assert len(p) == len(
        q), "both points must have the same number of dimensions"
    total = 0
    for i in range(len(p)):
        total += abs(p[i] + q[i])
    return total


def storage_dir() -> str:
    """寻找文件存储位置。"""
    if "MCPYPATH" in environ:
        mcpypath = environ["MCPYPATH"]
    elif sys.platform == "darwin":
        mcpypath = path.join(path.expanduser(
            "~"), "Library", "Application Support", "mcpy")
    else:
        mcpypath = path.join(path.expanduser("~"), ".mcpy")
    return mcpypath


def tex_coord(region: pyglet.image.TextureRegion, size=2048):
    """返回纹理的顶点。"""
    x, y = region.x, region.y
    d = 1 / size
    dx, dy = x * d / 16, y * d / 16
    return dx, dy, dx + d, dy, dx + d, dy + d, dx, dy + d
