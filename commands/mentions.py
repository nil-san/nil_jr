from discord.ext import commands
from nil_jr.db import cursor, is_active_subscriber
from nil_jr.utils import make_embed, subscriber_only
from datetime import datetime

class Mentions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ---------- Subscriber-only ----------
    @commands.command()
    @subscriber_only()
    async def mentions(self, ctx, limit: int = 10):
        """Show your recent mentions (max 20)"""
        user_id = ctx.author.id
        limit = max(1, min(limit, 20))  # enforce 1-20 limit

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
            try:
                ts_formatted = datetime.fromisoformat(ts).strftime("%Y-%m-%d %H:%M UTC")
            except Exception:
                ts_formatted = ts
            desc += f"**{i}.** [Jump to message]({url})\n🕒 `{ts_formatted}`\n\n"

        await ctx.send(embed=make_embed("Your Mentions", desc))

    # ---------- Owner-only ----------
    @commands.command()
    async def mentionsof(self, ctx, user: commands.UserConverter, limit: int = 10):
        """Show mentions of another user (Owner only, max 20)"""
        if ctx.author.id != self.bot.owner_id:
            return

        limit = max(1, min(limit, 20))

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
            try:
                ts_formatted = datetime.fromisoformat(ts).strftime("%Y-%m-%d %H:%M UTC")
            except Exception:
                ts_formatted = ts
            desc += f"**{i}.** [Jump to message]({url})\n🕒 `{ts_formatted}`\n\n"

        await ctx.send(embed=make_embed(f"Mentions of {user.mention}", desc))


# ---------- Async setup for discord.py v2 ----------
async def setup(bot):
    await bot.add_cog(Mentions(bot))
