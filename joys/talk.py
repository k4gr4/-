# joys/talk.py
import discord
from datetime import datetime, timedelta
import random

# ===== 設定 =====
RARE_CHANCE = 0.33     # 2%
RARE_MIN_HOURS = 1
RARE_MAX_HOURS = 2

# ===== 状態管理 =====
rare_until: datetime | None = None

def check_and_update_persona() -> bool:
    """
    現在が裏人格(レア)モードかどうかを判定・更新して返します。
    Trueなら裏人格、Falseなら通常人格です。
    """
    global rare_until
    now = datetime.now()

    # 1. すでに裏人格期間中なら True
    if rare_until and now < rare_until:
        return True

    # 2. 期間終了していたらリセット
    if rare_until and now >= rare_until:
        rare_until = None

    # 3. 新しく抽選 (2%の確率)
    if random.random() < RARE_CHANCE:
        duration_hours = random.randint(RARE_MIN_HOURS, RARE_MAX_HOURS)
        rare_until = now + timedelta(hours=duration_hours)
        return True
    
    return False

# ===== セリフ（メンション用） =====
def rare_persona_msg(hour: int) -> str:
    # 裏エリザ：冷淡、気だるげ、少し支配的
    if hour < 5:
        return "……まだ起きてるの？ 体に悪いことするの、好きだねぇ。"
    elif hour < 12:
        return "おはよ。朝から真面目ぶって、疲れない？"
    elif hour < 18:
        return "休憩しなよ。サボっちゃえばいいのに。"
    else:
        return "お疲れ。もう全部放り出して寝ちゃえば？"

def normal_persona_msg(hour: int) -> str:
    # 表エリザ：清楚、敬虔、世話焼き
    if 5 <= hour < 9:
        return "おはようございます。 今日も良い朝ですね。"
    elif 9 <= hour < 12:
        return "作業は順調ですか？"
    elif 12 <= hour < 14:
        return "お昼はもう召し上がりました？"
    elif 14 <= hour < 18:
        return "少しお疲れではありませんか？"
    elif 18 <= hour < 22:
        return "今日もお疲れ様でした🌙"
    else:
        return "夜更かしはほどほどに…"

def get_talk_reply():
    """メンション時の返答を取得"""
    is_rare = check_and_update_persona()
    hour = datetime.now().hour
    
    if is_rare:
        return rare_persona_msg(hour)
    else:
        return normal_persona_msg(hour)

def setup_talk(bot: discord.Client):
    @bot.event
    async def on_message(message: discord.Message):
        if message.author.bot:
            return

        if bot.user in message.mentions:
            reply = get_talk_reply()
            await message.reply(reply)

# joys/talk.py の最後の方に追加してください

def check_and_update_persona() -> bool:
    """現在の人格状態を確認し、裏人格ならTrueを返します"""
    global rare_until
    now = datetime.now()

    # すでに裏人格期間中か
    if rare_until and now < rare_until:
        return True

    # 期間終了
    if rare_until and now >= rare_until:
        rare_until = None
    
    # 新しく抽選 (2%)
    if random.random() < RARE_CHANCE:
        duration_hours = random.randint(RARE_MIN_HOURS, RARE_MAX_HOURS)
        rare_until = now + timedelta(hours=duration_hours)
        return True
    
    return False