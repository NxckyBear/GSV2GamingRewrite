import discord
from discord.ext import commands
import aiosqlite
import asyncio

from ...Data.dbconnect import connect_execute
from ...view.community.tempchannel import TempchannelView
from ...libs.bot import GSV2Bot
from ...libs.embeds import CustomEmbed

class TempchannelCog(commands.Cog):
    def __init__(self, bot: GSV2Bot):
        self.bot = bot
        self.init_db()
        self.temp_channels = {}
        self.bot.add_view(TempchannelView())

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel and not before.channel and after.channel.id == 1216646094776438814:  # HIER DIE CHANNEL ID VOM VOICE
            channel_info = await connect_execute(self.bot.cdb, "SELECT * FROM voice_channels WHERE user_id = ?", (member.id,), datatype="One")
            if not channel_info:
                channel_name = f"{member.name}'s Channel"
                category = member.guild.get_channel(1203327799373594644)  # HIER DIE CATEGORIE ID

                if not category:
                    return print("Channel wurde nicht gefunden")

                voice_channel = await member.guild.create_voice_channel(channel_name, category=category)
                await member.move_to(voice_channel)

                await connect_execute(self.bot.cdb, "INSERT INTO voice_channels (user_id, channel_id) VALUES (?, ?)", (member.id, voice_channel.id))
                if before.channel and len(before.channel.members) == 0:
                    await before.channel.delete()

                self.temp_channels[member.id] = voice_channel.id
                embed = CustomEmbed(title="Neuer Voice Channel", description=f"Willkommen in deinem eigenen Voice Channel, {member.mention}!")
                embed.set_thumbnail(url=member.guild.icon)
                await voice_channel.send(content=f"{member.mention}", embed=embed, view=TempchannelView())

        if before.channel and before.channel.id in self.temp_channels.values():
            if len(before.channel.members) == 0:
                await before.channel.delete()
                await connect_execute(self.bot.cdb, "DELETE FROM voice_channels WHERE channel_id = ?", (before.channel.id,))


async def setup(bot):
    await bot.add_cog(TempchannelCog(bot))