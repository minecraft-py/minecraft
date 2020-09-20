@echo off

echo "[install requirements]"
pip install -r requirements.txt >> nul
echo "[register]"
python3 register
echo "[copy files]"
pause
