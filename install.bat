@echo off

echo "[install requirements]"
pip install -r requirements.txt >> nul
echo "[register]"
python3 register
echo "[copy files]"
if not exist %MCPYPATH%\settings.json (
	copy data\json\settings.json /A %MCPYPATH%\settings.json
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
pause
