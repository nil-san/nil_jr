from discord.ext import commands
import discord
from nil_jr.db import is_active_subscriber

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        """
        Sends a help message showing only commands the user can run.
        """
        user_id = ctx.author.id
        is_owner = user_id == self.bot.owner_id
        is_subscriber = is_active_subscriber(user_id)

        embed = discord.Embed(
            title="Nil Jr Bot Commands",
            description="Here are the commands you can use:",
            color=discord.Color.blurple()
        )

        # Mentions commands
        if is_owner or is_subscriber:
            embed.add_field(
                name="Mentions Commands",
                value="`!n mentions [limit]` — Show your recent mentions\n"
                      "`!n mentionsof <user> [limit]` *(Owner only)* — Show mentions of a user",
                inline=False
            )

        # Subscriber management (Owner only)
        if is_owner:
            embed.add_field(
                name="Subscriber Commands (Owner only)",
                value="`!n addsub <user>` — Add subscriber\n"
                      "`!n removesub <user>` — Remove subscriber\n"
                      "`!n enablesub <user>` — Enable subscriber\n"
                      "`!n disablesub <user>` — Disable subscriber\n"
                      "`!n subscribers` — List all subscribers",
                inline=False
            )

        # Owner commands
        if is_owner:
            embed.add_field(
                name="Owner Commands",
                value="`!n shutdown` — Shut down the bot\n"
                      "`!n status <status_type> <activity_type> <activity_text>` — Change bot status",
                inline=False
            )

        embed.set_footer(text="Bot created by Nil-san | Prefix: !n")
        await ctx.send(embed=embed, delete_after=10)


async def setup(bot):
    await bot.add_cog(Help(bot))
