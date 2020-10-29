@echo off

echo "[install requirements]"
pip install -r requirements.txt >> nul
echo "[register]"
python3 register.py
echo "[copy files]"
if not exist %MCPYPATH%\settings.json (
	copy data\json\settings.json %MCPYPATH%\settings.json
)
if exist %MCPYPATH%\save (
	echo %0: %MCPYPATH%\save existed
) else (
	mkdir %MCPYPATH%\save
)
if exist %MCPYPATH%\screenshot (
	echo %0: %MCPYPATH%\screenshot existed
) else (
	mkdir %MCPYPATH%\screenshot
)
if exist %MCPYPATH%\texture\default (
	mkdir %MCPYPATH%\texture\default
	xcopy data\texture\* %MCPYPATH%\texture\default /sy
) else (
	del %MCPYPATH%\texture\default\*
	xcopy data\texture\* %MCPYPATH%\texture\default /sy
)
pause
