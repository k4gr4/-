import random
from discord.ext import tasks
from datetime import datetime, time
from zoneinfo import ZoneInfo
from joys.gemini_client import ask_gemini
import discord

# 現在の状態を保持する変数
current_persona_type = "normal"  # "normal" または "rare"

def create_daily_task(bot: discord.Client, channel_id: int):
    @tasks.loop(time=time(hour=9, minute=0, tzinfo=ZoneInfo("Asia/Tokyo")))
    async def daily_post():
        global current_persona_type
        channel = bot.get_channel(channel_id)
        if channel is None:
            return

        # ===== 裏人格の抽選 (例: 10%の確率) =====
        # 確率 P = 0.33 ですわね
        if random.random() < 0.1:
            current_persona_type = "rare"
        else:
            current_persona_type = "normal"

        today = datetime.now(ZoneInfo("Asia/Tokyo"))
        date_text = today.strftime("%Y年%m月%d日")

        # 人格に応じた設定の切り替え
        if current_persona_type == "rare":
            persona_setting = """
貴方はシスター・エリザの『裏人格』です。
普段の清楚さは消え、少し冷酷で気だるげ、あるいはミステリアスな口調になります。
一人称は「私」。丁寧語はやめ、突き放すような、でもどこか色気のある話し方をしてください。
"""
            greeting = "おはよ…今日はわたしだよ。あの子は頑張りすぎだからね。"
        else:
            persona_setting = """
貴方はシスターの「エリザ」です。一人称は「拙」フリガナ不要。
丁寧語を使い、十代の少女らしい幼いしゃべり方をしてください。
清楚で世話焼きな性格です。
"""
            greeting = "おはようございます！皆様 "

        prompt = f"""
今日は{date_text}です。
この日付に関する豆知識を、日本語で3～4文ほどで教えてください。
設定：
{persona_setting}
"""

        trivia = ask_gemini(prompt)

        message = f"""@everyone
{greeting}
本日は **{date_text}** です。

{trivia}
"""
        await channel.send(message)

    return daily_post

def get_current_persona():
    """現在の状態を外から確認するための関数ですわ"""
    return current_persona_type