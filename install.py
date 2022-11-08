#!/usr/bin/env python3

import uuid
from json import dump, load
from os import chmod, environ, makedirs, mkdir, path
from re import match, search
from stat import S_IRUSR, S_IWUSR, S_IXUSR
from subprocess import run
from sys import argv, executable, platform, version_info

step = 1


def main():
    # 最好遵守Mojang的Minecraft eula
    see_eula()
    # 检查python版本
    check_ver()
    # 安装
    install()
    # 注册玩家
    register_user()
    # 创建启动脚本
    gen_script()
    # 完成！
    if platform.startswith("win"):
        pycmd = "py"
    else:
        pycmd = "python3"
    print("Use `%s -m minecraft` to start game." % pycmd)


def check_ver():
    if version_info[:2] < (3, 8):
        print("Minecraft-in-python needs python3.8 or later, but %s found!" %
              ".".join([str(s) for s in version_info[:2]]))
        exit(1)


def gen_script():
    global step
    if "--skip-gen-script" in argv:
        return
    print("Step %d: Generate startup script" % step)
    step += 1
    while True:
        ret = input("Generate startup script[Y/n]? ")
        if (ret.lower() == "y") or (len(ret) == 0):
            break
        elif ret.lower() == "n":
            return
    script = ""
    name = get_file("run.sh")
    if platform.startswith("win"):
        name = get_file("run.bat")
        script += "@echo off\n"
    else:
        script += "#!/usr/bin/env sh\n"
    script += "cd \"%s\"\n" % path.dirname(get_file("install.py"))
    script += "\"%s\" -m minecraft\n" % executable
    with open(name, "w+") as f:
        f.write(script)
        print("Startup script at `%s`" % name)
    if not platform.startswith("win"):
        chmod(name, S_IRUSR | S_IWUSR | S_IXUSR)


def get_file(f):
    # 返回文件目录下的文件名
    return path.abspath(path.join(path.dirname(__file__), f))


def get_version():
    # 从`minecraft/utils/utils.py`文件里面把版本号"抠"出来
    f = open(path.join(get_file("minecraft"),
             "utils", "utils.py"), encoding="utf-8")
    start_find = False
    for line in f.readlines():
        if line.strip() == "VERSION = {":
            start_find = True
        elif (line.strip() == "}") and start_find:
            start_find = False
        elif line.strip().startswith("\"str\"") and start_find:
            # 匹配版本号
            # 一位主版本号, 两位小版本号/修订版本号
            # 匹配 -alpha, -beta 后缀, -pre, -rc 后跟数字
            return search(r"\d(\.\d{1,2}){2}(\-alpha|\-beta|\-pre\d+|\-rc\d+)?", line.strip()).group()


def install():
    global step
    MCPYPATH = search_mcpy()
    version = get_version()
    if not path.isdir(MCPYPATH):
        mkdir(MCPYPATH)
    install_settings()
    for name in ["log", "saves", "screenshot", "resource-pack"]:
        if not path.isdir(path.join(MCPYPATH, name)):
            mkdir(path.join(MCPYPATH, name))
    if not path.isdir(path.join(MCPYPATH, "lib", version)):
        makedirs(path.join(MCPYPATH, "lib", version))
    if "--skip-install-requirements" not in argv:
        print("Step %s: Install requirements" % step)
        step += 1
        code = run([executable, "-m", "pip", "install", "-U",
                   "-r", get_file("requirements.txt")]).returncode
        if code != 0:
            exit(1)


def install_settings():
    MCPYPATH = search_mcpy()
    source = {
        "fov": 70,
        "lang": "${auto}",
        "resource-pack": ["${default}"],
        "viewport": {
            "width": 800,
            "height": 600
        }
    }
    target = {}
    if path.isfile(path.join(MCPYPATH, "settings.json")):
        target = load(open(path.join(MCPYPATH, "settings.json")))
    for k, v in source.items():
        if k not in target or not isinstance(target[k], type(v)):
            target[k] = v
    dump(target, open(path.join(MCPYPATH, "settings.json"), "w+"))


def register_user():
    global step
    if "--skip-register" in argv:
        return
    print("Step %d: Register" % step)
    step += 1
    MCPYPATH = search_mcpy()
    is_ready = True
    previous_uuid = None
    # 如果之前已经存在玩家信息
    if path.isfile(path.join(MCPYPATH, "player.json")):
        player = load(open(path.join(MCPYPATH, "player.json")))
        # 是否符合当前的数据格式呢？
        try:
            for key, value in player.items():
                if not match("^[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}$", key):
                    is_ready = False
                if "name" not in value:
                    is_ready = False
        except:
            is_ready = False
        # 如果不符合，将之前的uuid记录下来（如果存在的话）
        if is_ready == False:
            s = open(path.join(MCPYPATH, "player.json"), "r").read()
            if (result := search("\"[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}\"", s)) is not None:
                previous_uuid = result.group(0)[1:-1]
    else:
        is_ready = False
    if not is_ready:
        player_id = previous_uuid or str(uuid.uuid4())
        print("Your uuid is %s, do not change it!" % player_id)
        player_name = ""
        while all([c for c in map(lambda c: any(
                [c.isalpha(), c.isdigit(), c == "_"]), player_name)]) and len(player_name) < 3:
            player_name = input("Your name: ")
        dump({player_id: {"name": player_name}}, open(
            path.join(MCPYPATH, "player.json"), "w+"), indent="\t")
        print(
            "Regsitered successfully, you can use your id to play multiplayer game!")
    else:
        print("You have regsitered!")


def search_mcpy():
    # 搜索文件存储位置
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


def see_eula():
    print("NOTE: This is not official Minecraft product. Not approved by or associated with Mojang.")
    print("      Visit `https://minecraft.net/term` for more information.")
    input("NOTE: Press ENTER when you have finished reading the above information: ")


if __name__ == "__main__":
    main()
