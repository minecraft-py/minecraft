# Copyright 2020-2022 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

import time
from os import environ, path
from sys import platform
from typing import Tuple, Union

import pyglet

start_time = time.strftime("%Y-%m-%d_%H.%M.%S")
_log_str = []
_have_colorama = False
try:
    from colorama import Fore, Style, init
    init()
    _have_colorama = True
except ModuleNotFoundError:
    pass

# 一个方块周围6个方块的相对坐标
FACES = [
    (0, 1, 0),
    (0, -1, 0),
    (1, 0, 0),
    (-1, 0, 0),
    (0, 0, 1),
    (0, 0, -1),
]

# Game version.
VERSION = {
    "major": 0,
    "minor": 3,
    "patch": 2,
    "str": "0.3.2",
    "data": 1
}


def log_err(text: str, name: str = "client", where: str = "cl"):
    """打印错误日志。"""
    if "l" in where:
        _log_str.append("[ERR  %s %s] %s" %
                        (time.strftime("%H:%M:%S"), name, text))
    if "c" in where:
        if _have_colorama:
            print("%s[ERR  %s %s]%s %s" % (Fore.RED, time.strftime(
                "%H:%M:%S"), name, Style.RESET_ALL, text))
        else:
            print("[ERR  %s %s] %s" % (time.strftime("%H:%M:%S"), name, text))


def log_info(text: str, name: str = "client", where: str = "cl"):
    """打印普通日志。"""
    if "l" in where:
        _log_str.append("[INFO %s %s] %s" %
                        (time.strftime("%H:%M:%S"), name, text))
    if "c" in where:
        if _have_colorama:
            print("%s[INFO %s %s]%s %s" % (Fore.GREEN, time.strftime(
                "%H:%M:%S"), name, Style.RESET_ALL, text))
        else:
            print("[INFO %s %s] %s" % (time.strftime("%H:%M:%S"), name, text))


def log_warn(text: str, name: str = "client", where: str = "cl"):
    """打印警告日志。"""
    if "l" in where:
        _log_str.append("[WARN %s %s] %s" %
                        (time.strftime("%H:%M:%S"), name, text))
    if "c" in where:
        if _have_colorama:
            print("%s[WARN %s %s]%s %s" % (Fore.YELLOW, time.strftime(
                "%H:%M:%S"), name, Style.RESET_ALL, text))
        else:
            print("[WARN %s %s] %s" % (time.strftime("%H:%M:%S"), name, text))


def on_exit():
    """在退出时保存日志。

    你不应该调用这个函数，它由`atexit`在退出时自动调用。
    """
    _os = __import__("os")
    log_info("Save logs to `log/log-%s.log`" % start_time, where="c")
    log_info("Exit")
    with open(_os.path.join(search_mcpy(), "log", "log-%s.log" % start_time), "w+") as log:
        log.write("\n".join(_log_str))
    # 将当前日志文件再保存一份至"log-latest.log"
    with open(_os.path.join(search_mcpy(), "log", "log-latest.log"), "w+") as latest_log:
        latest_log.write("\n".join(_log_str))


def search_mcpy() -> str:
    """寻找文件存储位置。"""
    if "MCPYPATH" in environ:
        MCPYPATH = environ["MCPYPATH"]
    elif platform == "darwin":
        MCPYPATH = path.join(path.expanduser(
            "~"), "Library", "Application Support", "mcpy")
    elif platform.startswith("win"):
        MCPYPATH = path.join(path.expanduser("~"), "mcpy")
    else:
        MCPYPATH = path.join(path.expanduser("~"), ".mcpy")
    return MCPYPATH


def mdist(p: Union[int, float], q: Union[int, float]) -> Union[int, float]:
    """计算同一维度内的点p和q之间的距离。"""
    assert len(p) == len(
        q), "both points must have the same number of dimensions"
    total = 0
    for i in range(len(p)):
        total += abs(p[i] + q[i])
    return total


def get_game() -> pyglet.window.Window:
    """获取GameWindow类的实例。

    根据程序算法，只能存在一个`minecraft.scene.GameWindow`对象。

    若直接导入模块运行该函数会引发异常。
    """
    for w in pyglet.canvas.get_display().get_windows():
        if str(w).startswith('GameWindow'):
            return w
    raise RuntimeError("No game window found")


def get_size() -> Tuple[int, int]:
    """返回窗口大小。"""
    w = get_game()
    return w.width, w.height
