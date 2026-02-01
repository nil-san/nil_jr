import discord
from datetime import datetime
from discord.ext import commands
from nil_jr.db import is_active_subscriber  # use the global DB function

def make_embed(title: str, description: str, color=discord.Color.blurple()):
    """Return a nicely formatted discord.Embed with timestamp."""
    return discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=datetime.utcnow()
    )

def subscriber_only():
    """
    A check to allow only active subscribers or the owner to run the command.
    Automatically sends a red 'Access Denied' embed if check fails.
    """
    async def predicate(ctx):
        # Owner can always run any command
        if ctx.author.id == ctx.bot.owner_id:
            return True

        # Active subscriber check
        if is_active_subscriber(ctx.author.id):
            return True

        # Not allowed → send access denied message
        await ctx.send(embed=make_embed(
            "❌ Access Denied",
            "⚠️ DIAGNOSIS: ||Skill issue tbh||",
            color=discord.Color.red()
            #delete_after=30
        ))
        return False

    return commands.check(predicate)

def owner_only():
    """A check to allow only the bot owner to run the command."""
    async def predicate(ctx):
        if ctx.author.id == ctx.bot.owner_id:
            return True

        await ctx.send(embed=make_embed(
            "❌ Access Denied",
            "This command is restricted to nil?.",
            color=discord.Color.red()
            #delete_after=30
        ))
        return False

    return commands.check(predicate)
