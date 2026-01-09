import asyncio
import discord
from discord import app_commands

def setup_timer_command(bot: discord.Client):
    @bot.tree.command(
        name="timer",
        description="指定した分後に通知しますわ"
    )
    @app_commands.describe(minutes="何分後に通知しますか？")
    async def timer(interaction: discord.Interaction, minutes: int):
        if minutes <= 0:
            await interaction.response.send_message(
                "1分以上を指定してくださいまし 💦",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"{minutes}分後にお知らせいたしますわ ⏰"
        )

        await asyncio.sleep(minutes * 60)

        await interaction.followup.send(
            f"{interaction.user.mention} ⏰ {minutes}分経過しましたわ！"
        )
