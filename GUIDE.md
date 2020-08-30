# 安装指南
这是 Minecraft 的安装指南, 适用于菜鸟玩家.

# 下载 python3
Minecraft 使用 python3 作为开发语言, 使用了 3.8+ 版本的特性, 请安装 python3.8 及以后版本.

## Windows 用户
*虽然 Minecraft 在多平台都可以运行, 但是 Windows 作者极少使用, 如何安装python 请自行搜索, 这里只介绍 noise 包的安装*

noise 是 python 的一个噪声函数库, 一部分使用 C 编写, 如果大家没有安装 Visual Studio 14 可能会叫你安装之.

这里推荐一个不需要 Visual Studio 的方法:

1. 在浏览器打开 <https://www.lfd.uci.edu/~gohlke/pythonlibs/#noise>
2. 选择适合你 CPU 类型, 以及 python 版本的 wheel 包
3. 下载它(很快的, 不需要 VPN)
4. 打开终端, 输入`pip install <刚刚下载的 *.whl 包>`
5. 完成

## 类 UNIX 用户
在不同的发行版有不同的包管理器, 这里举两个例子:
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
```
git clone htts://github.com/jason-bowen-zheng/Minecraft
# 中国境内用户使用下面这行
git clone https://gitee.com/jason-bowen-zheng/Minecraft
```

没有 Git, 下载并解压:
```
https://github.com/jason-bowen-zheng/Minecraft/archive/master.zip
# 或
https://gitee.com/jason-bowen-zheng/Minecraft/repository/archive/master.zip
```
