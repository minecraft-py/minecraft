#!/usr/bin/sh

echo "[install requirements]"
pip install -r requirements.txt >> /dev/null
echo "[register]"
python3 register.py
echo "[copy files]"
if test -d $MCPYPATH
then
	# 复制 settings.json
	if test ! -e $MCPYPATH/settings.json
		cp data/json/settings.json $MCPYPATH/settings.json
	then
		echo "$0: $MCPYPATH/settings.json existed"
	fi
	# 复制 window.json
	if test ! -e $MCPYPATH/window.json
		cp data/json/window.json $MCPYPATH/window.json
	then
		echo "$0: $MCPYPATH/window.json existed"
	fi
	# 创建 save/ 目录
	if test ! -d $MCPYPATH/save
	then
		mkdir $MCPYPATH/save
	else
		echo "$0: $MCPYPATH/save existed"
	fi
	# 创建 screenshot/ 目录
	if test ! -d $MCPYPATH/screenshot
	then
		mkdir $MCPYPATH/screenshot
	else
		echo "$0: $MCPYPATH/screenshot existed"
	fi
	# 复制游戏贴图
	if test ! -d $MCPYPATH/texture/default
	then
		mkdir $MCPYPATH/texture/default -p
		cp data/texture/* $MCPYPATH/texture/default -r
	else
		rm $MCPYPATH/texture/default/* -r
		cp data/texture/* $MCPYPATH/texture/default -r
	fi
else
	echo "$0: MCPYPATH path not found"
fi
