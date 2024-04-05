import discord
from discord.ext import commands
import requests
import random
import string
import asyncio
from datetime import datetime
import pytz

TOKEN = '' # discord bot token
GUILD_ID = '' # server id
CHANNEL_IDS = [''] # channel id that bot send users

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

                with open("logs.txt", "a") as f:
                    f.write(f"{username}\n")
                
                embed = discord.Embed(
                    title=f"💫 Scraped new user",
                    description="⭐ https://github.com/kellyhated/RobloxGen-Short-Usernames",
                    color=discord.Color.blurple()
                )
                embed.set_footer(text=f"V1.0.5 | {current_time}")
                embed.set_author(name="⚡ Kelly 5 Chars Scraper", icon_url="https://cdn.discordapp.com/attachments/1224383101174812672/1225806855947943976/e496fd15afc37f773f3f2f6ddf5006ca.jpg?ex=66227898&is=66100398&hm=9e2fdc08e1db7e95b29f45f2f448580417bc8dd7847bbf5f9ad0e1f46fd4e6aa&")  # Set the author as your bot with its icon
                embed.set_thumbnail(url=None)
                
                # Add fields to the embed
                embed.add_field(name="👤 User", value=username, inline=True)
                embed.add_field(name="✨ Register here", value="[Register page](https://www.roblox.com/signup)", inline=True)
                print(f"scraped new user {username}")
                await channel.send(embed=embed)
        await asyncio.sleep(1)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name=".gg/tdDUKaS4Py"))
    await scrape_usernames()    

bot.run(TOKEN)
