# 安装指南
这是 Minecraft 的简明安装指南, 适用于菜鸟玩家 或 没有安装 python 的玩家.

# 下载 python3
Minecraft 使用 python3 作为开发语言, 使用了 3.8+ 版本的特性, 请安装 python3.8 及以后版本.

## Windows 用户
*文档暂缺*

## 类 UNIX 用户
在不同的发行版有不同的包管理器, 这里举两个作者用过的 Linux 发行版的例子:
> 如果往后真正运行 Minecraft 时发现没有 pip 和 tk 的可以再安装

Debian:
```shell
# 或许需要使用 root 权限
apt update
apt upgrade
apt install python3
```

Arch Linux:
```shell
# 或许需要 root 权限
pacman -Syu
pacman -S python3
```

题外话, Termux:
```shell
# 该项目原本就是设计可以在 Termux 上完美运行的(就是 fps 只有1)
pkg upgrade
pkg install clang
pkg install python
pkg install python-tkinter
```

# 下载 Minecraft 源代码及资源
Minecraft 源代码托管在 Github 和 Gitee(中国境内), Gitee 同 Github 同步更新.

如果有 Git, 那么输入:
```shell
git clone htts://github.com/jason-bowen-zheng/Minecraft
# Gitee(中国境内)
git clone https://gitee.com/jason-bowen-zheng/Minecraft
```

没有 Git, 下载并解压到`Minecraft`目录:
```shell
wget https://github.com/jason-bowen-zheng/Minecraft/archive/master.zip
# 或
wget https://gitee.com/jason-bowen-zheng/Minecraft/repository/archive/master.zip
```

# 游玩前步骤
首先, 必须确定文件复制位置, 可以有如下两种选择:

- 默认的
  - Windows 在`%HOME%\mcpy\`目录下
  - Linux/MacOS 在`~/.mcpy`目录下
- 设置一个`MCPYPATH`环境变量, 值为游戏文件复制的位置.
> 程序会检查是否存在`MCPYPATH`环境变量

然后, 运行`install.py`就可以了.

## 注册
注册程序非常简单, 会使用`uuid`库来生成一个随机的 uuid.

你必须起一个名字, 最少两个字符(ASCII 字符 + 数字 + 下划线). 其中, 第一个字符不能为数字.

# 游玩
在 Windows, 双击`Minecraft.bat`即可启动启动器.

在类 UNIX, 输入`python -m Minecraft`同样可以启动启动器.

或者在`~/.bashrc`添加如下内容:
```shell
alias mcpy="cd ~/Minecraft && python -m Minecraft && cd - >> /dev/null"
```

