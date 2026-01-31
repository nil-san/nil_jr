import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", 0))

if not BOT_TOKEN:
    raise RuntimeError("DISCORD_TOKEN not set")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=["!n", "!n "], intents=intents)

# Pass OWNER_ID to cogs if needed
bot.owner_id = OWNER_ID

# Load cogs
bot.load_extension("events.on_message")
bot.load_extension("commands.mentions")
bot.load_extension("commands.subscribers")

bot.run(BOT_TOKEN)
