#!/usr/bin/env python3

from json import dump, load
from os import chmod, environ, listdir, mkdir, makedirs, path, system
from re import search
from shlex import join
from shutil import rmtree
from sys import argv, executable, platform, version_info
from stat import S_IRUSR, S_IWUSR, S_IXUSR
from subprocess import run
import uuid
from zipfile import ZipFile

def main():
    # 最好遵守 Mojang 的 Minecraft eula
    see_eula()
    if "--travis-ci" in argv:
        do_travis_ci()
    # 检查 python 版本
    check_ver()
    # 安装
    install()
    # 注册玩家
    register_user()
    # 创建启动脚本
    gen_script()
    # 完成!
    if platform.startswith("win"):
        pycmd = "py"
    else:
        pycmd = "python3"
    print("Use `%s -m minecraft` to start game." % pycmd)
    print("[Done]")

def check_ver():
    if version_info[:2] < (3, 8):
        print("Minecraft-in-python need python3.8 or later, but %s found." % ".".join([str(s) for s in version_info[:2]]))
        if "--travis-ci" in argv:
            exit(0)
        else:
            exit(1)

def do_travis_ci():
    # 专门给 Travis CI 使用, 也可以检测代码是否有语法错误
    print("[Travis CI]")
    print("python version: %s" % ".".join([str(s) for s in version_info[:3]]))
    print("Minecraft-in-python version: %s" % get_version())
    # 检测模糊缩进
    print("[Travis CI > Check tabnanny]")
    output = run([executable, "-m", "tabnanny", "-v", get_file("minecraft")], capture_output=True)
    lines = output.stderr.decode().split("\n")
    failed = False
    for line in lines:
        if "Indentation Error:" in line:
            print("Check failed: %s(line %s)" % (line[1: line.find(":") - 1], line[line.rindex(" ") + 1: -1]))
            failed = True
    else:
        if failed:
            exit(1)
        else:
            print("Pass")

def gen_script():
    if "--skip-gen-script" in argv:
        return
    print("[Generate startup script]")
    while True:
        if "--travis-ci" in argv:
            break
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
    if "--travis-ci" in argv:
        with open("run.sh", "r") as f:
            print("[Generate startup script > start run.sh]")
            print(f.read()[:-1])
            print("[Generate startup script > end   run.sh]")

def get_file(f):
    # 返回文件目录下的文件名
    return path.abspath(path.join(path.dirname(__file__), f))

def get_version():
    # 从 minecraft/utils/utils.py 文件里面把版本号"抠"出来
    f = open(path.join(get_file("minecraft"), "utils", "utils.py"), encoding="utf-8")
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
    if ("--skip-install-requirements" not in argv) and ("--travis-ci" not in argv):
        print("[Install requirements]")
        pip = "\"%s\" -m pip" % executable
        if "--hide-output" in argv:
            code = system("%s install -U -r %s >> %s" % (pip, get_file("requirements.txt"), path.devnull))
        else:
            code = system("%s install -U -r %s" % (pip, get_file("requirements.txt")))
        if code != 0:
            print("pip raise error code: %d" % code)
            exit(1)
        else:
            print("install successfully")
    else:
        print("[Skip install requirements]")

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
    # 离线注册
    if ("--skip-register" not in argv) and ("--travis-ci" not in argv):
        print("[Register]")
        MCPYPATH = search_mcpy()
        if not path.isfile(path.join(MCPYPATH, "player.json")):
            player_id = str(uuid.uuid4())
            print("Your uuid is %s, do not change it" % player_id)
            player_name = ""
            is_valid_char = lambda c: any([c.isalpha(), c.isdigit(), c == "_"])
            while all([c for c in map(is_valid_char, player_name)]) and len(player_name) < 3:
                player_name = input("Your name: ")
            dump({"id": player_id, "name": player_name}, open(path.join(MCPYPATH, "player.json"), "w+"), indent="\t")
            print("Regsitered successfully, you can use your id to play multiplayer game!")
        else:
            print("You have regsitered!")
    else:
        print("[Skip regsiter]")

def search_mcpy():
    # 搜索文件存储位置
    if "MCPYPATH" in environ:
        MCPYPATH = environ["MCPYPATH"]
    elif platform == "darwin":
        MCPYPATH = path.join(path.expanduser("~"), "Library", "Application Support", "mcpy")
    elif platform.startswith("win"):
        MCPYPATH = path.join(path.expanduser("~"), "mcpy")
    else:
        MCPYPATH = path.join(path.expanduser("~"), ".mcpy")
    return MCPYPATH

def see_eula():
    print("NOTE: This is not official Minecraft product. Not approved by or associated with Mojang.")
    print("      Visit `https://minecraft.net/term` for more information.")
    if "--travis-ci" not in argv:
        input("NOTE: Press ENTER when you have finished reading the above information: ")

if __name__ == "__main__":
    main()
