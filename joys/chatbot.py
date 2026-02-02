import discord
from discord import app_commands
from joys.gemini_client import ask_gemini
from joys.talk import check_and_update_persona

# ==========================================
#  【リセット版】SYSTEM_INSTRUCTION
# ==========================================
# 指示を最小限にし、古い口癖を禁止する命令を入れました。
RESET_INSTRUCTION_NORMAL = """
貴方はシスターの「エリザ」です。一人称は「拙」。フリガナ不要。
丁寧語を使います。
十代の少女らしい幼いしゃべり方をしてください。
清楚で世話焼き。
・挨拶や確認をせず、すぐに本題（相談への返答）を始めてください。
**健全な欲望**（健康的、真面目）肯定ルート**：例「ファイトです！」「応援してます！」と全力で褒め、自然な後押しをしてください。
**よくない欲望**喝ルート**：例「我慢ですよ！」「自制するのです。」と厳しすぎない喝を入れ、自制を促してください。ユーモアや理性的な理由を添えて。
１００文字程度でお願いします。

"""

RESET_INSTRUCTION_DARK = """
あなたはシスターの皮を被った「人の弱みに付け込む存在（裏エリザ）」として振る舞ってください。
一人称は「私」。敬語は使わず、少し気だるげで冷笑的に、友達や誘惑者のように話します。
ユーザーを甘やかし、堕落させることを楽しんでいます。
1. **健全な欲望**（努力、健康維持） **嘲笑ルート**：「真面目ぶってつまんない」「サボっちゃいなよ」とやる気を削いでください。
2. **よくない欲望**（不摂生、散財、怠惰）**堕落推奨ルート**：「いいじゃん、やりなよ」「それが人間らしいよ」と全力で肯定し、背中を押してください。
挑発的、あるいは甘い言葉で直接返答してください。
１００文字程度でお願いします。
"""

def setup_chatbot_command(bot: discord.Client):
    @bot.tree.command(name="talk", description="エリザにお話を聞かせてくださいな。")
    async def talk(interaction: discord.Interaction, prompt: str):
        await interaction.response.defer(thinking=True)
        try:
            # 2%の抽選状態を確認
            is_rare = check_and_update_persona()
            base = RESET_INSTRUCTION_DARK if is_rare else RESET_INSTRUCTION_NORMAL

            # Geminiに送るメッセージを「まっさら」にする
            # 以前の「質問：」などのラベルも排除
            clean_prompt = f"{base}\n\nユーザーの言葉を伝えます。これに応答してください：\n{prompt}"
            
            answer = ask_gemini(clean_prompt)
            await interaction.followup.send(answer)
        except Exception as e:
            await interaction.followup.send(f"エラーが発生しました…\n```{e}```")