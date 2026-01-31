import discord
from discord.ext import commands
from db import add_subscriber, remove_subscriber, enable_subscriber, disable_subscriber, cursor, is_active_subscriber
from utils import make_embed

class Subscribers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def addsub(self, ctx, user: commands.UserConverter):
        if ctx.author.id != self.bot.owner_id:
            return
        add_subscriber(user.id)
        await ctx.send(embed=make_embed("Subscriber Added", f"{user.mention} has been added ✅"))

    @commands.command()
    async def removesub(self, ctx, user: commands.UserConverter):
        if ctx.author.id != self.bot.owner_id:
            return
        remove_subscriber(user.id)
        await ctx.send(embed=make_embed("Subscriber Removed", f"{user.mention} has been removed ❌", color=discord.Color.red()))

    @commands.command()
    async def enablesub(self, ctx, user: commands.UserConverter):
        if ctx.author.id != self.bot.owner_id:
            return
        enable_subscriber(user.id)
        await ctx.send(embed=make_embed("Subscriber Enabled", f"{user.mention} has been enabled 🟢"))

    @commands.command()
    async def disablesub(self, ctx, user: commands.UserConverter):
        if ctx.author.id != self.bot.owner_id:
            return
        disable_subscriber(user.id)
        await ctx.send(embed=make_embed("Subscriber Disabled", f"{user.mention} has been disabled 🔴", color=discord.Color.red()))

    @commands.command()
    async def subscribers(self, ctx):
        if ctx.author.id != self.bot.owner_id:
            return
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

def setup(bot):
    bot.add_cog(Subscribers(bot))
