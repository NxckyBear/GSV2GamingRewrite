import asyncio
import discord
from discord.ext import commands
from discord.ui import View, Button
from ...libs.bot import GSV2Bot
from ...libs.embeds import CustomEmbed
from ...view.community.bugforum import CustomView


class ForumCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1170464267808542853
        self.bot.add_view(CustomView())  

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        if thread.parent_id == self.channel_id:
            await self.post_custom_message(thread)

    async def post_custom_message(self, thread):
        embed = CustomEmbed(title='Bug Report', description='Das Team bedankt sich für den Report.\nWir setzen uns unverzüglich an die Arbeit\n\nDanke das du die GSv Community so fleißig unterstützt.')
        view = CustomView()
        await asyncio.sleep(3)
        await thread.send(file=self.bot.file, embed=embed, view=view)

def setup(bot):
    bot.add_cog(ForumCog(bot))