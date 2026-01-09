from discord.ext import tasks
from datetime import datetime, time
from zoneinfo import ZoneInfo
from gemini_client import ask_gemini
import discord

def create_daily_task(bot: discord.Client, channel_id: int):
    @tasks.loop(time=time(hour=9, minute=0, tzinfo=ZoneInfo("Asia/Tokyo")))
    async def daily_post():
        channel = bot.get_channel(channel_id)
        if channel is None:
            print("投稿チャンネルが見つかりませんでした…")
            return

        today = datetime.now(ZoneInfo("Asia/Tokyo"))
        date_text = today.strftime("%Y年%m月%d日")

        prompt = f"""
今日は{date_text}です。
この日付に関する豆知識を、
日本語で、３～４文ほどで教えてください。
この時一人称は拙で、発言の終わりには「本日も皆様にとって良い日でありますように。」とつけてください。
また、謙虚な様子の文でお願いします。拙にフリガナはいりません。
"""

        trivia = ask_gemini(prompt)

        message = f"""@everyone
おはようございます！皆様 ☀  
本日は **{date_text}** ですよ。

{trivia}
"""
        await channel.send(message)

    return daily_post