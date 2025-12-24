import discord
from discord import app_commands
import aiohttp
from bs4 import BeautifulSoup
import urllib.parse
import os
from keep_alive import keep_alive  # เรียกใช้ฟังก์ชันกันหลับ

# --- ใส่ TOKEN ใหม่ของคุณตรงนี้ ---
BOT_TOKEN = os.getenv('TOKEN')

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print("Synced commands successfully.")

client = MyClient()

# --- 1. ฟังก์ชันดึงชื่อเกม (Steam API) ---
async def get_steam_game_name(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if data and str(appid) in data and data[str(appid)]['success']:
                    return data[str(appid)]['data']['name']
    return None

# --- 2. ฟังก์ชันเช็คไฟล์ Fix (Scraping OnlineFix) ---
async def check_onlinefix_status(game_name):
    safe_name = urllib.parse.quote_plus(game_name)
    search_url = f"https://online-fix.me/index.php?do=search&subaction=search&story={safe_name}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(search_url, headers=headers) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    articles = soup.find_all("div", class_="article")
                    return len(articles) > 0
    except:
        return False
    return False

# --- 3. ฟังก์ชันดึง DRM (Scraping Steam Store โดยตรง) ---
async def get_drm_notice(appid):
    url = f"https://store.steampowered.com/app/{appid}/"
    cookies = {'birthtime': '631180801', 'mature_content': '1'}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36"}

    try:
        async with aiohttp.ClientSession(cookies=cookies) as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    drm_div = soup.find("div", class_="DRM_notice")
                    
                    if drm_div:
                        drm_text = drm_div.get_text(strip=True)
                        return drm_text.replace("Incorporates 3rd-party DRM:", "").strip()
                    
                    if "Denuvo" in html:
                        return "Denuvo Anti-Tamper (Detected in text)"
                        
    except Exception as e:
        print(f"Error checking DRM: {e}")
    
    return "Not provided"

# --- คำสั่ง Slash Command ---
@client.tree.command(name="ezfix", description="เช็คสถานะเกมและ DRM")
@app_commands.describe(steam_appid="ใส่เลข AppID ของ Steam")
async def ezfix(interaction: discord.Interaction, steam_appid: str):
    
    await interaction.response.defer()

    game_name = await get_steam_game_name(steam_appid)
    if not game_name:
        await interaction.followup.send(f"❌ ไม่พบข้อมูล AppID: {steam_appid}")
        return

    has_onlinefix = await check_onlinefix_status(game_name)
    drm_info = await get_drm_notice(steam_appid)

    online_txt = "✅ Available" if has_onlinefix else "❌ Unavailable"
    bypass_txt = "✅ Available" if has_onlinefix else "❌ Unavailable" 

    embed = discord.Embed(
        title=game_name,
        url=f"https://store.steampowered.com/app/{steam_appid}/",
        color=discord.Color.from_rgb(46, 204, 113) if has_onlinefix else discord.Color.from_rgb(231, 76, 60)
    )
    
    embed.add_field(name="AppID", value=f"`{steam_appid}`", inline=True)
    
    drm_display = f"⚠️ {drm_info}" if "Denuvo" in drm_info else drm_info
    embed.add_field(name="DRM Notice", value=f"```{drm_display}```", inline=False)

    sources_value = (
        f"**OnlineFix:** {online_txt}\n"
        f"**Bypasses:** {bypass_txt}"
    )
    embed.add_field(name="Sources", value=sources_value, inline=False)
    
    search_link = f"https://online-fix.me/index.php?do=search&subaction=search&story={urllib.parse.quote_plus(game_name)}"
    embed.add_field(name="Manual Check", value=f"[Click here to search]({search_link})", inline=False)
    
    embed.set_thumbnail(url=f"https://cdn.cloudflare.steamstatic.com/steam/apps/{steam_appid}/header.jpg")
    embed.set_footer(text=f"Request by {interaction.user.name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)

    await interaction.followup.send(embed=embed)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# --- ส่วนสำคัญ: สั่งเปิด Web Server ก่อนรันบอท ---
keep_alive()
client.run(BOT_TOKEN)