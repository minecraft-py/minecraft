# Javascript 函数
Minecraft 为 js 定义了数量众多的 api, 用来操控世界:

```javascript
addBlock(x, y, z, block);
```
添加方块的函数

- `x, y, z` - 方块的坐标
- `block` - 方块的名称(如`grass`)
> `block`为`air`则移除坐标处方块

```javascript
getBlock(x, y, z);
```
返回坐标处的方块

- `x, y, z` - 方块的坐标
> 如果方块不存在, 返回字符串`air`

```javascript
getGLlib(s);
```
返回`pyglet.gl`库中的常数或函数

- `s` - 对象名称(如`glColor3f`)
> 对象`s`不存在则返回`null`. 返回的函数是可以运行的

```javascript
getSettings(key);
```
返回`$MCPYPATH/settings.json`的内容

- `key` - 要返回的键值
> 键不存在返回`null`

```javascript
loadGLlib(s);
```
与`getGLlib`类似, 但是直接定义一个函数, 没有返回值.
> 该函数封装了`getGLlib`函数

```javascript
logInfo(s);
```
打印信息

- `s` - 要打印的内容
> 同样的, 还有`logErr`, `logWarn`函数用于显示不同的消息前缀

```javascript
removeBlock(x, y, z);
