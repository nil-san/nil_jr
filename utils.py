import discord
from datetime import datetime

def make_embed(title: str, description: str, color=discord.Color.blurple()):
    return discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=datetime.utcnow()
    )
