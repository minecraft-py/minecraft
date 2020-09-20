@echo off

echo "[install requirements]"
pip install -r requirements.txt >> nul
echo "[register]"
python3 register
echo "[copy files]"
if not exist %MCPYPATH%\settings.json copy data\json\settings.json /A %MCPYPATH%\settings.json
mkdir %MCPYPATH%\save
mkdir %MCPYPATH%\screenshot
pause
