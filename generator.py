import discord
from discord.ext import commands
import requests
import random
import string
import asyncio
from datetime import datetime
import pytz

TOKEN = 'MTEzNDE3NjA4MTkzNTYwNTg3Mg.G0iknh.QCeUI5l4OrfF4VKLLuvfJKvl_UO6nl46MFTq1Q'
GUILD_ID = '1142573954389790880'
CHANNEL_IDS = ['1173325602317664346']  # Добавьте все необходимые идентификаторы каналов
SCRAPER_VERSION = '2.0 Premium'

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

def generate_username(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def is_username_available(username):
    url = f"https://auth.roblox.com/v1/usernames/validate?birthday=2005-01-01&context=Signup&gender=female&username={username}"
    response = requests.get(url)
    data = response.json()
    return data.get("message") == "Username is valid"

async def scrape_usernames():
    while True:
        username = generate_username(5)
        if is_username_available(username):
            for channel_id in CHANNEL_IDS:
                channel = bot.get_channel(int(channel_id))
                
                tz = pytz.timezone('Europe/Kiev')
                current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
                
                embed = discord.Embed(
                    title="New Username Scraped!",
                    description=f"The available username is: ``{username}``\n**Time:** *{current_time}*",
                    color=discord.Color.dark_grey()
                )
                embed.set_footer(text=f"Scraper version: {SCRAPER_VERSION}")
                await channel.send(embed=embed)
        await asyncio.sleep(1)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="Checking roblox usernames..."))
    await scrape_usernames()    

bot.run(TOKEN)
