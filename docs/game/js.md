# Javascript
Minecraft 可以在某些特定的时刻运行 js. js 文件位于`$MCPYPATH/save/<存档名>/script.js`.
是一个存档目录的可选文件.

js 可以使用`require`函数.

# 回调函数
- `on_init` - 在游戏地图初始化之后调用

> 函数执行时间不要过长, Minecraft 没有为 js 的运行建立一个线程
