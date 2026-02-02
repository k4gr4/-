import aiohttp
import discord
from discord import app_commands

async def get_steam_wishlist_discounts():
    """Steam内部IDを使用して確実にウィッシュリストを取得しますわ"""
    # スクリーンショット(338)で確認できた、お嬢様の不変のIDです
    steam_id_numeric = "76561199526054234"
    url = f"https://store.steampowered.com/wishlist/profiles/{steam_id_numeric}/wishlistdata/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": f"https://steamcommunity.com/profiles/{steam_id_numeric}/wishlist"
    }
    
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.get(url) as response:
                content_type = response.headers.get("Content-Type", "")
                
                # HTMLが返ってきた場合、Steamがログイン画面などに飛ばした証拠ですわ
                if "text/html" in content_type:
                    return None, f"Steamがデータを拒否しましたわ。設定は公開なのに不思議ですわね…少し時間を置いて試してみてくださいまし。"

                if response.status != 200:
                    return None, f"Steam接続エラーですわ（Status: {response.status}）"
                
                data = await response.json()
                if not data:
                    return None, "ウィッシュリストは読み込めましたが、中身が空っぽのようですわ。"

                embed = discord.Embed(
                    title="🎁 Steamウィッシュリスト・セール速報", 
                    color=0x1b2838,
                    description="お嬢様、最新の割引情報を直接入手いたしましたわ！"
                )
                found_sale = False

                for app_id, game in data.items():
                    subs = game.get('subs', [])
                    if subs:
                        discount = subs[0].get('discount_pct', 0)
                        if discount > 0:
                            found_sale = True
                            name = game.get('name', '不明なタイトル')
                            # 100倍された価格を整数に戻します
                            price_raw = subs[0].get('price', 0)
                            price = price_raw // 100 if price_raw else "無料"
                            
                            embed.add_field(
                                name=name, 
                                value=f"**{discount}% OFF**\n価格: `{price}円` \n[ストアへ](https://store.steampowered.com/app/{app_id}/)", 
                                inline=True
                            )

                if not found_sale:
                    return None, "現在、ウィッシュリストの中にセール中のゲームはございませんでしたわ。"
                
                return embed, None

        except Exception as e:
            return None, f"申し訳ございません、技術的な問題が発生いたしました：{str(e)}"

def setup_steam_command(bot):
    @bot.tree.command(name="steam_wishlist", description="Steamから最新のセール情報を取得しますわ！")
    async def steam_wishlist(interaction: discord.Interaction):
        await interaction.response.defer()
        embed, error = await get_steam_wishlist_discounts()
        if error:
            await interaction.followup.send(error)
        else:
            await interaction.followup.send(embed=embed)