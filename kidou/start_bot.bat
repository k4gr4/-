@echo off
chcp 65001 > nul

:loop
cd /d "C:\Users\hl5sj\OneDrive\デスクトップ\DISCORD.BOT - バックアップ\DISCORD.BOT"

echo [%date% %time%] Botを起動します...
.venv\Scripts\python main.py >> bot.log 2>&1

echo [%date% %time%] Botが停止しました。10秒後に再起動します...
timeout /t 10 /nobreak > nul
goto loop
