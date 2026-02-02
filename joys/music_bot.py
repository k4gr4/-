import discord
from discord import app_commands
import yt_dlp
import random
import re
import asyncio

async def get_audio_info(url: str):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None,
        lambda: yt_dlp.YoutubeDL(YDL_OPTIONS).extract_info(url, download=False)
    )

YDL_OPTIONS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}

def setup_music_bot(bot: discord.Client, music_channel_id: int):
    youtube_urls: list[str] = []

    async def load_youtube_urls():
        nonlocal youtube_urls
        youtube_urls.clear()

        try:
            text_channel = await bot.fetch_channel(music_channel_id)
        except discord.NotFound:
            print("ライブハウス（音楽チャンネル）が見つからないぞ？")
            return

        pattern = re.compile(r"(https?://(www\.)?(youtube\.com|youtu\.be)/\S+)")
        async for message in text_channel.history(limit=200):
            if message.content:
                match = pattern.search(message.content)
                if match:
                    youtube_urls.append(match.group(1))
        print(f"URLを {len(youtube_urls)} 個読んだぜ！check it out！ 🎶")

    async def play_random(vc: discord.VoiceClient, text_channel: discord.TextChannel):
        if not youtube_urls:
            await load_youtube_urls()
        if not youtube_urls:
            await text_channel.send("再生できる奴がないぞ？ ")
            return

        url = random.choice(youtube_urls)

        info = await get_audio_info(url)
        audio_url = info["url"]
        title = info.get("title", "Unknown")


        source = discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS)

        def after_play(error):
            if error:
                print(f"再生エラーだな…: {error}")
            bot.loop.create_task(play_random(vc, text_channel))

        vc.play(source, after=after_play)
        await text_channel.send(f"🎶 再生中だぜ！：**{title}**")

    @bot.tree.command(
        name="music",
        description="音楽チャンネルからランダム再生（DJモード）でイクぜ！GO LIVE!"
    )
    async def music(interaction: discord.Interaction):
        await interaction.response.defer()

        if not interaction.user.voice:
            await interaction.followup.send(
                "聴衆がいないと始まらないだろ？先にボイスチャンネルへ言ってちょうだいな？ ",
                ephemeral=True
            )
            return

        voice_channel = interaction.user.voice.channel
        vc = interaction.guild.voice_client or await voice_channel.connect()

        if vc.is_playing():
            vc.stop()

        await play_random(vc, interaction.channel)
        await interaction.followup.send("🎧 ランダムD。モードを開始したぜ。")

    @bot.tree.command(
        name="stop",
        description="音楽再生を停止してボイスチャンネルから退出するぞ。BYE。 ⏹"
    )
    async def stop(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        vc = interaction.guild.voice_client
        if vc is None:
            await interaction.followup.send("今は、ボイスチャンネルには接続してないぞ。", ephemeral=True)
            return
        if vc.is_playing():
            vc.stop()
        await vc.disconnect()
        await interaction.followup.send("⏹ 音楽を止めて、退出するぜ。", ephemeral=True)
