# Minecraft
> 感谢 [这个项目](https://github.com/fogleman/Minecraft), 该项目源于此.

该项目是一个对 Minecraft Java版的复刻, 旨在使用 python 重写 Minecraft 并实现其中的大部分功能.
> 下文所提及的`Minecraft`都指该项目, 没有什么新的名字可以取了.

要游玩 Minecraft, 请先下载依赖项:
```shell
pip install -U pyglet glooey
# 其中, glooey 尚未使用, 是可选的
```

然后, 在 Windows 资源管理器下, 双击`Minecraft.pyw`即可运行.

其余系统输入: `python Minecraft.pyw`

# 最终目标
下面这个 TODO 列表是 Minecraft 要实现的功能:

- [x] 行为控制(已实现部分)
- [x] 世界生成
- [ ] 随机世界生成
- [ ] 更多方块
- [ ] 使用`E`键打开物品栏
- [ ] 与方块交互
- [ ] ...

# 控制角色

- `左键 右键` - 破坏和放置
- `W A S D` - 分别向前后左右移动
- `空格` - 跳跃
- `左SHIFT` - 疾跑
- `TAB` - 飞行与行走的切换
- `F2` - 截屏
- `ESC` - 退出游戏
- `数字键` - 切换物品(目前有三种物品: `草方块, 沙子, 砖块`和一种无法放置, 不能破坏的物品, 类似基岩, 但我改过材质)
