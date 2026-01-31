from discord.ext import commands
import discord

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        """
        Sends a simple help message with all main commands.
        """
        embed = discord.Embed(
            title="Nil Jr Bot Commands",
            description="Here are the main commands you can use:",
            color=discord.Color.blurple()
        )

        # Mentions Commands
        embed.add_field(
            name="Mentions Commands",
            value="`!n mentions [limit]` — Show your recent mentions\n"
                  "`!n mentionsof <user> [limit]` *(Owner only)* — Show mentions of a user",
            inline=False
        )

        # Subscriber Commands (Owner only)
        embed.add_field(
            name="Subscriber Commands (Owner only)",
            value="`!n addsub <user>` — Add subscriber\n"
                  "`!n removesub <user>` — Remove subscriber\n"
                  "`!n enablesub <user>` — Enable subscriber\n"
                  "`!n disablesub <user>` — Disable subscriber\n"
                  "`!n subscribers` — List all subscribers",
            inline=False
        )

        # Owner Commands
        embed.add_field(
            name="Owner Commands",
            value="`!n shutdown` — Shut down the bot\n"
                  "`!n status <status_type> <activity_type> <activity_text>` — Change bot status",
            inline=False
        )

        embed.set_footer(text="Bot created by Nil-san | Prefix: !n")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
