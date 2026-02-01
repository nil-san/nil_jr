import discord
from discord.ext import commands
from nil_jr.db import add_subscriber, remove_subscriber, enable_subscriber, disable_subscriber, cursor
from nil_jr.utils import make_embed, owner_only 

class Subscribers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ---------- Owner-only Commands ----------
    @commands.command()
    @owner_only()
    async def addsub(self, ctx, user: commands.UserConverter):
        add_subscriber(user.id)
        await ctx.send(embed=make_embed("Subscriber Added", f"{user.mention} has been added ✅"))

    @commands.command()
    @owner_only()
    async def removesub(self, ctx, user: commands.UserConverter):
        remove_subscriber(user.id)
        await ctx.send(embed=make_embed("Subscriber Removed", f"{user.mention} has been removed ❌", color=discord.Color.red()))

    @commands.command()
    @owner_only()
    async def enablesub(self, ctx, user: commands.UserConverter):
        enable_subscriber(user.id)
        await ctx.send(embed=make_embed("Subscriber Enabled", f"{user.mention} has been enabled 🟢"))

    @commands.command()
    @owner_only()
    async def disablesub(self, ctx, user: commands.UserConverter):
        disable_subscriber(user.id)
        await ctx.send(embed=make_embed("Subscriber Disabled", f"{user.mention} has been disabled 🔴", color=discord.Color.red()))

    @commands.command()
    @owner_only()
    async def subscribers(self, ctx):
        cursor.execute("SELECT user_id, enabled FROM subscribers")
        rows = cursor.fetchall()
        if not rows:
            await ctx.send(embed=make_embed("Subscribers", "No subscribers"))
            return

        desc = ""
        for uid, enabled in rows:
            status = "🟢 Enabled" if enabled else "🔴 Disabled"
            desc += f"<@{uid}> — {status}\n"

        await ctx.send(embed=make_embed("Subscribers", desc))

# ---------- Async setup ----------
async def setup(bot):
    await bot.add_cog(Subscribers(bot))
