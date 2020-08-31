# Minecraft 服务器
该目录是 Minecraft 多人联机游戏的总服务器

# 命令
以下命令是控制命令

## 登入登出服务器
- *join $id $name [$password]* - 加入服务器, 密码可以留空
- *passwd $id $password* - 玩家登录服务器设置的密码
- *leave $id* - 离开服务器

## 方块放置破坏
- *add $id $x $y $z $block* - 放置方块
- *remove $id $x $y $z* - 破坏方块

## 玩家相关
- *moveto $id $x $y $z* - 移动
- *lookat $id $rx $ry* - 视线方向
- *hotkey $id $block* - 玩家手持物品
- *throw $id $block $times* - 玩家丢出物品
- *get id $x $y $z* - 玩家拾起物品

## 杂项
- *dialogue $id $message* - 聊天
- *command $id $command* - 执行命令

# 服务器应答
- *ok* - 允许操作
- *no* - 禁止操作
- *unknow* - 未知操作
- *message $text* - 发送消息, text 应为能被`pyglet.text.decode_attributed()`解析的字符串
- *ban $reason* - 踢出游戏
