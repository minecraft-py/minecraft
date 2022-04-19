import atexit
import math
import time

start_time = time.strftime("%Y-%m-%d_%H.%M.%S")
log_str = []
_have_colorama = False
try:
    from colorama import Fore, Style, init
    init()
    _have_colorama = True
except ModuleNotFoundError:
    pass
import pyglet

# 一个方块周围6个方块的相对坐标
FACES = [
    ( 0, 1, 0),
    ( 0,-1, 0),
    ( 1, 0, 0),
    (-1, 0, 0),
    ( 0, 0, 1),
    ( 0, 0,-1),
]

# 版本号, "str"项用于外部程序以及直接显示
VERSION = {
    "major": 0,
    "minor": 3,
    "patch": 2,
    "str": "0.3.2",
    "data": 1
}

def log_err(text, name="client", where="cl"):
    # 打印错误信息
    # 于何处(where)
    # c(onsole) - 于标准输出中打印
    # l(og)     - 保存至日志文件
    if "l" in where:
        log_str.append("[ERR  %s %s] %s" % (time.strftime("%H:%M:%S"), name, text))
    if "c" in where:
        if _have_colorama:
            print("%s[ERR  %s %s]%s %s" % (Fore.RED, time.strftime("%H:%M:%S"), name, Style.RESET_ALL, text))
        else:
            print("[ERR  %s %s] %s" % (time.strftime("%H:%M:%S"), name, text))

def log_info(text, name="client", where="cl"):
    # 打印普通信息
    if "l" in where:
        log_str.append("[INFO %s %s] %s" % (time.strftime("%H:%M:%S"), name, text))
    if "c" in where:
        if _have_colorama:
            print("%s[INFO %s %s]%s %s" % (Fore.GREEN, time.strftime("%H:%M:%S"), name, Style.RESET_ALL, text))
        else:
            print("[INFO %s %s] %s" % (time.strftime("%H:%M:%S"), name, text))

def log_warn(text, name="client", where="cl"):
    # 打印警告信息
    if "l" in where:
        log_str.append("[WARN %s %s] %s" % (time.strftime("%H:%M:%S"), name, text))
    if "c" in where:
        if _have_colorama:
            print("%s[WARN %s %s]%s %s" % (Fore.YELLOW, time.strftime("%H:%M:%S"), name, Style.RESET_ALL, text))
        else:
            print("[WARN %s %s] %s" % (time.strftime("%H:%M:%S"), name, text))

@atexit.register
def on_exit():
    # 在退出时保存日志
    _os  = __import__("os")
    log_info("Save logs to "log/log-%s.log"" % start_time, where="c")
    log_info("Exit", where="c")
    with open(_os.path.join(search_mcpy(), "log", "log-%s.log" % start_time), "w+") as log:
        log.write("\n".join(log_str))
    # 将当前日志文件再保存一份至`log-latest.log`
    with open(_os.path.join(search_mcpy(), "log", "log-latest.log"), "w+") as latest_log:
        latest_log.write("\n".join(log_str))

def search_mcpy():
    # 寻找文件存储位置
    _os  = __import__("os")
    _sys = __import__("sys")
    platform = _sys.platform
    environ, path = _os.environ, _os.path
    if "MCPYPATH" in environ:
        MCPYPATH = environ["MCPYPATH"]
    elif platform == "darwin":
        MCPYPATH = path.join(path.expanduser("~"), "Library", "Application Support", "mcpy")
    elif platform.startswith("win"):
        MCPYPATH = path.join(path.expanduser("~"), "mcpy")
    else:
        MCPYPATH = path.join(path.expanduser("~"), ".mcpy")
    return MCPYPATH

def mdist(p, q):
    # 计算曼哈顿距离
    # 注意和 math.dist 的区别
    assert len(p) == len(q), "both points must have the same number of dimensions"
    total = 0
    for i in range(len(p)):
        total += abs(p[i] + q[i])
    return total
