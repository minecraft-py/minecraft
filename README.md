# Minecraft
> 感谢 [Fogleman](https://github.com/fogleman/Minecraft), 这个项目正是克隆于他的 Minecraft 项目, 并翻译了注释, 
添加了一些 PR 中的内容.

该项目是一个对 Minecraft Java版的复刻, 旨在使用 python 重写 Minecraft 并实现其中的大部分功能.
> 下文所提及的`Minecraft`都指该项目, 没有什么新的名字可以取了.

要游玩 Minecraft, 请先下载依赖项:
```shell
pip install -U pyglet kytten glooey
# 我正在考虑应该使用 kytten 还是 glooey 来实现复杂的 GUI
```

然后, 输入`python3 -m Minecraft`运行游戏, 可能需要一些时间.

# 最终目标
下面这个 TODO 列表是 Minecraft 要实现的功能:

- [ ] 启动器(使用 tkinter 实现)
- [x] 行为控制(已实现部分, 参见下面`控制角色`)
- [x] 世界生成
- [ ] 随机世界生成
- [ ] 更多方块
- [ ] 使用`E`键打开物品栏
- [ ] 与方块交互
- [ ] ...

# 控制角色
- `鼠标左键 右键` - 破坏和放置
- `W A S D` - 分别向前后左右移动
- `空格` - 跳跃
- `左SHIFT` - 疾跑
- `左Ctrl` - 潜行
- `TAB` - 飞行与行走的切换
- `F2` - 截屏
- `ESC` - 退出游戏
- `数字键` - 循环切换物品(目前有`草方块 泥土 沙子 石头`方块)
