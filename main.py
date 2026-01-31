import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

# ================= ENV =================
load_dotenv()
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", 0))

if not BOT_TOKEN:
    raise RuntimeError("DISCORD_TOKEN not set")

# ================= BOT SETUP =================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=["!n", "!n "], intents=intents)
bot.owner_id = OWNER_ID  # Make owner_id accessible in cogs

# ================= ASYNC START =================
async def main():
    async with bot:
        # Load cogs (await required in discord.py v2)
        await bot.load_extension("events.on_message")
        await bot.load_extension("commands.mentions")
        await bot.load_extension("commands.subscribers")

        # Start bot
        await bot.start(BOT_TOKEN)

# Run the async main function
asyncio.run(main())
