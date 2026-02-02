import sys
from pathlib import Path
import discord

def setup(bot):
    @bot.tree.command(
        name="saiki",
        description="Botを安全に停止します（管理者用）"
    )
    async def saiki(interaction: discord.Interaction):

        # 管理者チェック（必要なければ消してOK）
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "このコマンドは管理者専用です。",
                ephemeral=True
            )
            return

        # 停止フラグ作成
        stop_file = Path("STOP_BOT.txt")
        stop_file.touch()

        await interaction.response.send_message(
            "停止命令を受け取りました。Botを停止します…",
            ephemeral=True
        )

        await bot.close()
        sys.exit(0)
