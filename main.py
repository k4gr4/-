import discord
from discord import app_commands
import os
from dotenv import load_dotenv
import asyncio
from joys.gemini_client import ask_gemini
from joys.daily import create_daily_task
from joys.music_bot import setup_music_bot  # 音楽再生機能
import sys
from pathlib import Path
from joys.chatbot import setup_chatbot_command  # ←これを追加しますわ
from joys.talk import setup_talk
from joys.steam import setup_steam_command
from joys.steam import setup_steam_command
# ===== .env 読み込み =====
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
DAILY_CHANNEL_ID = int(os.getenv("CHANNEL_ID"))       # デイリー投稿用
MUSIC_CHANNEL_ID = int(os.getenv("MUSIC_CHANNEL_ID")) # 音楽再生用

if not DISCORD_TOKEN or not GUILD_ID or not DAILY_CHANNEL_ID or not MUSIC_CHANNEL_ID:
    raise RuntimeError("環境変数が不足しておりますね…！")


class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # メッセージ履歴取得に必要ですわ
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        guild = discord.Object(id=int(GUILD_ID))
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

        # デイリー投稿タスクを作成
        self.daily_task = create_daily_task(self, DAILY_CHANNEL_ID)
        self.daily_task.start()

        print("Bot起動完了です！")


bot = MyClient()

# ===== 音楽BOTのセットアップ =====
setup_music_bot(bot, MUSIC_CHANNEL_ID)


from joys.dice import setup_dice_command
setup_dice_command(bot)

# ===== タイマーコマンドのセットアップ =====
from timer import setup_timer_command
setup_timer_command(bot)

# ===== チャット機能のセットアップ（追加！） =====
setup_chatbot_command(bot)

setup_talk(bot)

# ===== テスト用コマンド =====
@bot.tree.command(name="daily_test", description="朝の投稿テストですよ！")
async def daily_test(interaction: discord.Interaction):
    await interaction.response.send_message("テスト投稿を行わせていただきます…")
    await bot.daily_task()

from kanrisya.saiki import setup as saiki_setup

saiki_setup(bot)

setup_steam_command(bot)

# ===== Bot 起動 =====
bot.run(DISCORD_TOKEN)
