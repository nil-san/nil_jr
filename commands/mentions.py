from discord.ext import commands
from db import cursor, is_active_subscriber
from utils import make_embed

class Mentions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mentions(self, ctx, limit: int = 10):
        user_id = ctx.author.id
        if user_id != self.bot.owner_id and not is_active_subscriber(user_id):
            return

        cursor.execute(
            "SELECT message_url, timestamp FROM mentions WHERE target_id = ? ORDER BY id DESC LIMIT ?",
            (user_id, limit)
        )
        rows = cursor.fetchall()

        if not rows:
            await ctx.send(embed=make_embed("Mentions", "No mentions logged 👍"))
            return

        desc = ""
        for i, (url, ts) in enumerate(rows, 1):
            desc += f"**{i}.** [Jump to message]({url})\n🕒 `{ts}`\n\n"

        await ctx.send(embed=make_embed("Your Mentions", desc))

    @commands.command()
    async def mentionsof(self, ctx, user: commands.UserConverter, limit: int = 10):
        if ctx.author.id != self.bot.owner_id:
            return

        cursor.execute(
            "SELECT message_url, timestamp FROM mentions WHERE target_id = ? ORDER BY id DESC LIMIT ?",
            (user.id, limit)
        )
        rows = cursor.fetchall()

        if not rows:
            await ctx.send(embed=make_embed("Mentions", f"No mentions found for {user.mention}"))
            return

        desc = ""
        for i, (url, ts) in enumerate(rows, 1):
            desc += f"**{i}.** [Jump to message]({url})\n🕒 `{ts}`\n\n"

        await ctx.send(embed=make_embed(f"Mentions of {user}", desc))

def setup(bot):
    bot.add_cog(Mentions(bot))