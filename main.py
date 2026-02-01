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

bot = commands.Bot(
    command_prefix=["n!", "n! "],
    intents=intents,
    help_command=None  # Disable default help
)
bot.owner_id = OWNER_ID  # Make owner_id accessible in cogs

# ================= EVENT: READY =================
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")
    # Default status/activity
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name="Nil Jr Bot")
    )

# ================= ASYNC START =================
async def main():
    async with bot:
        # ---------- Load cogs ----------
        await bot.load_extension("nil_jr.events.on_message")
        await bot.load_extension("nil_jr.commands.mentions")
        await bot.load_extension("nil_jr.commands.subscribers")
        await bot.load_extension("nil_jr.commands.help")
        await bot.load_extension("nil_jr.commands.owner")

        # ---------- Start bot ----------
        await bot.start(BOT_TOKEN)

# ================= RUN =================
if __name__ == "__main__":
    # Use asyncio.run() safely
    asyncio.run(main())
