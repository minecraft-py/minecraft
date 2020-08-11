# Minecraft
> 感谢 [Fogleman](https://github.com/fogleman/Minecraft), 这个项目正是克隆于他的 Minecraft 项目, 并翻译了注释, 
添加了一些 PR 中的内容.

该项目是一个对 Minecraft Java版的复刻, 旨在使用 python 重写 Minecraft 并实现其中的大部分功能.

Minecraft 支持多平台, 使用 GPL 开源, 在配置低的电脑上也可以很好的运行.
> 该 README 所提及的`Minecraft`都指该项目, 没有什么新的名字可以取了.

要游玩 Minecraft, 请先下载依赖项:
```shell
pip install -U pyglet kytten glooey
# 我正在考虑应该使用 kytten 还是 glooey 来实现复杂的 GUI
```

然后, 输入`python3 -m Minecraft`运行游戏, 可能需要一些时间来加载.

# 最终目标
下面这个 TODO 列表是 Minecraft 要实现的功能:

- [x] 行为控制(已实现部分, 参见下面`控制角色`)
- [x] 更多方块
- [x] 与方块交互
- [x] 世界生成
- [x] 随机世界生成(使用 Simplex 噪声, 但世界唯一)
- [ ] 启动器(使用 tkinter 实现)
- [ ] 更多地形
- [ ] 使用`E`键打开物品栏
- [ ] ...

# 控制角色
- `鼠标左键 鼠标右键` - 破坏 和 放置(交互)
- `W A S D` - 移动玩家
- `空格` - 跳跃
- `左Shift` - 疾跑
- `左Ctrl` - 潜行(不改变高度), 在交互方块的毗邻放置方块
- `TAB` - 飞行与行走的切换
- `F2` - 截屏
- `ESC` - 退出游戏
- `数字键` - 循环切换物品(目前有9种方块)
