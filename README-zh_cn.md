> 感谢 [fogleman](https://github.com/fogleman/Minecraft), 这个项目正是克隆于他的 Minecraft 项目
[English](README.md) | 简体中文

# Minecraft
用 python 做开源的 Minecraft

## 游玩
要游玩 Minecraft, 请先在终端输入:
```shell
# 非中国用户使用下面这行
git clone https://github.com/jason-bowen-zheng/Minecraft
# 位于中国的用户使用下面这行
git clone https://gitee.com/jason-bowen-zheng/Minecraft
cd Minecraft
pip install -r requirements.txt
./register
```

在 Windows 上, 双击`Minecraft.bat`运行启动器.

如果你在使用 Bash, 可以在`~/.bashrc`或`/etc/.profile`写入:
```shell
alias Minecraft="cd ~/Minecraft && python3 -m Minecraft && cd - >> /dev/null"
```
来快速启动 Minecraft.

# 最终目标
下面这个 TODO 列表是 Minecraft 要实现的功能:

- [x] 行为控制(已实现部分, 参见下面`控制角色`)
- [x] 更多方块
- [x] 与方块交互
- [x] 世界生成
- [x] 随机世界生成(使用 Simplex 噪声, 现已移除)
- [x] 启动器(使用 tkinter 实现, 十分简陋)
- [x] i18n
- [x] 保存用户对世界的更改
- [ ] 更多地形
- [ ] 区块系统
- [ ] 使用`E`键打开物品栏
- [ ] ...

# 控制角色
- `鼠标左键 鼠标右键` - 破坏 和 放置(交互)
- `W A S D` - 移动玩家
- `空格` - 跳跃 或 在飞行中上升高度
- `ENTER` - 死亡后重生
- `数字键` - 循环切换物品(目前有9种方块)
- `左Ctrl` - 疾跑
- `左Shift` - 潜行(不改变高度), 在交互方块的毗邻放置方块 或 在飞行中降低高度
- `TAB` - 飞行与行走的切换
- `F2` - 截屏
- `F3` - 拓展功能(先按`F3`, 松开, 再按下一个按键)
  - `P` - 显示玩家坐标
  - `R` - 强制疾跑(飞行忽略)
- `F11` - 切换全屏
- `ESC` - 退出游戏

# 贡献者
感谢以下的开发者的贡献:

- [wzh656](https://github.com/wzh656)
