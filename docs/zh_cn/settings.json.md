# settings.json
`settings.json`是 Minecraft 的配置文件, 可以控制部分游戏内容.

每次打开游戏, Minecraft 都会检查`settings.json`是否合规. 如果不合规, 那么会给出错误原因, 并退出游戏.

`settings.json`各个键的意义:

- `fov` - 玩家的视角场, 范围从`50(最小值)`到`100(最大值)`
- `lang` - 启动器与游戏语言(在`data/json/lang`目录中, 不存在的语言会报错)
- `use-theme` - 启动器使用的主题(在`Minecraft/theme`目录下, 不存在的主题会报错)

报错内容:

- `settings.json: missing '<键>' key` - 规定的键没有设置(未规定的可以存在)
- `settings.json: language '<设置的语言>' not found` - 未找到目标语言
- `settings.json: theme '<设置的主题>' not found` - 未找到目标主题
