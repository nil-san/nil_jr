from discord.ext import commands
import discord
from nil_jr.utils import make_embed, owner_only

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ---------- Shutdown command ----------
    @commands.command()
    @owner_only()
    async def shutdown(self, ctx):
        """Shut down the bot"""
        await ctx.send(embed=make_embed("Shutdown", "Shutting down... 👋", color=discord.Color.red()))
        await self.bot.close()

    # ---------- Change bot status & activity ----------
    @commands.command(name="status")
    @owner_only()
    async def change_status(self, ctx, status_type: str = None, activity_type: str = None, *, activity_text: str = None):
        """
        Change the bot's status and activity.
        Usage examples:
        !n status online playing Chess
        !n status dnd watching Tutorials
        !n status idle listening Music
        !n status invisible competing Coding
        """
        # If no arguments provided, show usage
        if not (status_type and activity_type and activity_text):
            await ctx.send(embed=make_embed(
                "Usage: !n status",
                "Example:\n`!n status online playing Chess`\n"
                "`!n status dnd watching Tutorials`\n"
                "`!n status idle listening Music`\n"
                "`!n status invisible competing Coding`"
            ))
            return

        # Map status_type to discord.Status
        status_map = {
            "online": discord.Status.online,
            "dnd": discord.Status.dnd,
            "idle": discord.Status.idle,
            "invisible": discord.Status.invisible
        }
        status = status_map.get(status_type.lower())
        if not status:
            await ctx.send(embed=make_embed(
                "❌ Invalid Status",
                f"Choose from: {', '.join(status_map.keys())}",
                color=discord.Color.red()
            ))
            return

        # Map activity_type to discord.ActivityType
        activity_map = {
            "playing": discord.ActivityType.playing,
            "watching": discord.ActivityType.watching,
            "listening": discord.ActivityType.listening,
            "competing": discord.ActivityType.competing
        }
        activity_type_obj = activity_map.get(activity_type.lower())
        if not activity_type_obj:
            await ctx.send(embed=make_embed(
                "❌ Invalid Activity",
                f"Choose from: {', '.join(activity_map.keys())}",
                color=discord.Color.red()
            ))
            return

        activity = discord.Activity(type=activity_type_obj, name=activity_text)
        await self.bot.change_presence(status=status, activity=activity)

        await ctx.send(embed=make_embed(
            "✅ Status Updated",
            f"Status: **{status_type.title()}**\nActivity: **{activity_type.title()} {activity_text}**"
        ))

# ---------- Async setup for discord.py v2 ----------
async def setup(bot):
    await bot.add_cog(Owner(bot))
