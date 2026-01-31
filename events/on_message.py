from discord.ext import commands
from db import is_active_subscriber, cursor, conn
from datetime import datetime

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        targets = []

        # Direct mentions
        for user in message.mentions:
            if user.id == self.bot.owner_id or is_active_subscriber(user.id):
                targets.append(user.id)

        # Replies
        if message.reference and message.reference.message_id:
            try:
                ref = await message.channel.fetch_message(message.reference.message_id)
                if ref.author.id == self.bot.owner_id or is_active_subscriber(ref.author.id):
                    targets.append(ref.author.id)
            except:
                pass

        # Log mentions
        for target_id in set(targets):
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

        if targets:
            conn.commit()

        await self.bot.process_commands(message)

def setup(bot):
    bot.add_cog(OnMessage(bot))
