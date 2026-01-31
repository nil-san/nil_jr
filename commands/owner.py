from discord.ext import commands
import discord

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Shutdown command
    @commands.command()
    async def shutdown(self, ctx):
        if ctx.author.id != self.bot.owner_id:
            return
        await ctx.send("Shutting down... 👋")
        await self.bot.close()

    # Change bot status & activity
    @commands.command(name="status")
    async def change_status(self, ctx, status_type: str, activity_type: str, *, activity_text: str):
        """
        Change the bot's status and activity.
        Usage:
        !n status online playing Chess
        !n status dnd watching Tutorials
        !n status idle listening Music
        !n status invisible playing Hide and Seek
        """

        if ctx.author.id != self.bot.owner_id:
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
            await ctx.send(f"❌ Invalid status type. Choose from: {', '.join(status_map.keys())}")
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
            await ctx.send(f"❌ Invalid activity type. Choose from: {', '.join(activity_map.keys())}")
            return

        activity = discord.Activity(type=activity_type_obj, name=activity_text)
        await self.bot.change_presence(status=status, activity=activity)
        await ctx.send(f"✅ Status updated: `{status_type}` with `{activity_type} {activity_text}`")

def setup(bot):
    bot.add_cog(Owner(bot))
