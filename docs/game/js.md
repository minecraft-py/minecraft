# javascript
Minecraft 可以在某些特定的时刻运行 javascript. javascript 文件位于`$MCPYPATH/<存档名>/script.js`. 是一个存档目录的可选文件.

javascript 可以使用`require`函数.

# 回调函数
- `on_init` - 在游戏地图初始化之后调用

# Minecraft 定义的函数
```javascript
function add_block(x, y, z, block);
```
添加方块的函数

- `x, y, z` - 方块的坐标
- `block` - 方块的名称(如`grass`)

- - -

```javascript
function get_block(x, y, z);
```
返回坐标处的方块

- `x, y, z` - 方块的坐标

如果方块不存在, 返回字符串`air`

- - -

```javascript
function remove_block(x, y, z);
```
移除坐标处的方块

- `x, y, z` - 方块的坐标

- - -

```javascript
function test_block(x, y, z, block);
```
检测坐标处的方块, 相等返回`true`, 否则返回`false`

- `x, y, z` - 方块的坐标
- `block` - 检测方块的类型

没有任何方块为`air`
