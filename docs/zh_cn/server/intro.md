# 服务器
服务器位于`server/`目录下, 相对应的游戏客户端位于`Minecraft/client.py`文件.

可以通过控制台(`console`)来控制服务器

## 命令行参数
在`Minecraft`目录下使用`python -m server ...`来启动服务器, 命令行参数如下:

- `server` - 启动服务器(默认值)
- `console` - 启动控制台
- `setpass` - 设置服务器密码
- `help` - 显示帮助

## 控制台
控制台(`console`)类似于一个运行在命令行下 web 应用.

## 更改密码
使用`python -m server setpass`来更改密码, 会要求输入原密码以及确认两次新密码.

新的密码会写回`$MCPYAPTH/server.json`文件中, **不要更改它!**
