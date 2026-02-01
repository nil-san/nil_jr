from discord.ext import commands
from nil_jr.db import is_active_subscriber, cursor, conn
from datetime import datetime

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Skip bots
        if message.author.bot:
            return

        targets = set()  # Use a set to avoid duplicates

        # ---------- Direct mentions ----------
        for user in message.mentions:
            if user.id == self.bot.owner_id or is_active_subscriber(user.id):
                targets.add(user.id)

        # ---------- Replies ----------
        if message.reference and message.reference.message_id:
            try:
                ref = await message.channel.fetch_message(message.reference.message_id)
                if ref.author.id == self.bot.owner_id or is_active_subscriber(ref.author.id):
                    targets.add(ref.author.id)
            except Exception:
                pass  # ignore if message not found

        # ---------- Log mentions ----------
        if targets:
            for target_id in targets:
                cursor.execute(
                    """
                    INSERT INTO mentions
                    (target_id, author_id, channel_id, guild_id, message_url, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        target_id,
                        message.author.id,
                        message.channel.id,
                        message.guild.id if message.guild else None,
                        message.jump_url,
                        datetime.utcnow().isoformat()
                    )
                )
            conn.commit()

        # ---------- Process commands ----------
        # Only process commands once per message
        if message.content.startswith(tuple(self.bot.command_prefix)):
            await self.bot.process_commands(message)


async def setup(bot):
    # Add cog asynchronously (discord.py v2)
    await bot.add_cog(OnMessage(bot))
