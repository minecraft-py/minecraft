# 简介
该项目计划使用 python 复刻一个原版 Minecraft 的效果, 并想结合 Minecraft Java 版 和 Minecraft 基岩版 的特性.

# 最低游戏配置
- 内存: 1G 左右(由于 python 也是很费内存的, 可以的话 2G)
- 外部存储空间: 100M 左右(源代码 + 资源包 + 游戏存储, 其实也只需要 5M 以内)
- 显卡: Intel 的~~非常垃圾的~~集成显卡就可以了, 再垃圾也会有至少 60 FPS

# 依赖项
依赖项的版本为开发机使用的版本或该依赖项的最高版本, 定义在`requirements.txt`中:

- `Js2Py>=0.70`: 运行 javascript 的 python 库
- `psutil>=5.7.2`: 检测游戏重复启动
- `pyglet>=1.5.11`: OpenGL 库
- `pyshaders>=1.4.1`: 编译与链接 GLSL
- `opensimplex>=0.3`: 简单的 Simplex 噪声函数库
- `...`: 随着开发进度的增加会有更多的依赖项

> `Js2Py`有非常严重的 bug. 在解决完成之前, 不要编写 js 供 Minecraft 运行!
