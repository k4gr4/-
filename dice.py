import discord
from discord import app_commands
import random
import re


DICE_PATTERN = re.compile(r"^(\d+)[dD](\d+)$")


def setup_dice_command(bot: discord.Client):

    @bot.tree.command(
        name="dice",
        description="NdN ダイスを振らさせていただきます。（例: 2d6, 1d100）🎲"
    )
    @app_commands.describe(
        dice="NdN 形式で入力してください。（例: 3d6）"
    )
    async def dice(interaction: discord.Interaction, dice: str):
        match = DICE_PATTERN.match(dice)

        if not match:
            await interaction.response.send_message(
                "形式が正しくありませんよ。💦 `NdN`（例: `2d6`）で入力してください。",
                ephemeral=True
            )
            return

        count = int(match.group(1))   # n（振る個数）
        sides = int(match.group(2))   # N（面数）

        # 安全制限（暴走防止）
        if count <= 0 or sides <= 0 or count > 100 or sides > 1000:
            await interaction.response.send_message(
                "ダイスの数は1〜100、面数は1〜1000までにしてくださいね 🎲",
                ephemeral=True
            )
            return

        rolls = [random.randint(1, sides) for _ in range(count)]
        total = sum(rolls)

        await interaction.response.send_message(
            f"🎲 **{count}d{sides} の結果です！**\n"
            f"出目：{', '.join(map(str, rolls))}\n"
            f"合計：**{total}**"
        )
