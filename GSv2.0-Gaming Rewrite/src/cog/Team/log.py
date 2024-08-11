import discord
from discord.ext import commands
import datetime
from ...libs.bot import GSV2Bot
from ...libs.embeds import CustomEmbed

CHANID = 1218317295345074298
class Log(commands.Cog):

    def __init__(self, bot: GSV2Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user} has connected to Discord!')

    @commands.Cog.listener("on_member_join")
    async def log_member_join(self, member):
        em = CustomEmbed(
            title="Member Joined",
            description=f"**Nutzer**: {member.name}"
                        f'\r\n**Joined Server**: {member.joined_at.strftime("%d.%m.%Y %H:%M")}'
                        f'\r\n**Account Created**: {member.created_at.strftime("%d.%m.%Y %H:%M")}',
            timestamp=datetime.datetime.now())

        channel = await self.bot.fetch_channel(CHANID)

        if channel:
            await channel.send(file=self.bot.file, embed=em)

    @commands.Cog.listener("on_guild_channel_create")
    async def log_on_guild_channel_create(self, channel):
        em = CustomEmbed(
            title="Channel wurde erstellt",
            description=f"**Channel Erstellt**: {channel.mention}",
            timestamp=datetime.datetime.now())

        chan = await self.bot.fetch_channel(CHANID)

        if chan:
            await channel.send(file=self.bot.file, embed=em)

    @commands.Cog.listener("on_guild_channel_delete")
    async def log_on_guild_channel_delete(self, channel):
        em = CustomEmbed(
            title="Channel wurde gelöscht",
            description=f"**Channel wurde gelöscht**: {channel.mention}",
            timestamp=datetime.datetime.now())

        chan = await self.bot.fetch_channel(CHANID)

        if chan:
            await channel.send(file=self.bot.file, embed=em)

    @commands.Cog.listener("on_member_update")
    async def log_update_member(self, before, after):
        if len(before.roles) > len(after.roles):
            role = next(role for role in before.roles if role not in after.roles)
            em = CustomEmbed(
                title="Rollenänderung",
                description=f"**Name**: {before}\r\n**Entfernte Rolle:**: {role.name}",
                timestamp=datetime.datetime.now())

        elif len(after.roles) > len(before.roles):
            role = next(role for role in after.roles if role not in before.roles)
            em = CustomEmbed(
                title="Rollenänderung",
                description=f"**Name**: {before}\r\n**Neue Rolle:**: {role.name}",
                timestamp=datetime.datetime.now())

        elif before.nick != after.nick:
            em = CustomEmbed(
                title="Nickname wurde geändert!",
                description=f"**Name**: {before}\r\n**Alter NickName**: {before.nick}\r\n**Neuer NickName**: {after.nick}",
                timestamp=datetime.datetime.now())

        else:
            return
        channel = await self.bot.fetch_channel(CHANID)

        if channel:
            await channel.send(file=self.bot.file, embed=em)

    @commands.Cog.listener("on_message_edit")
    async def log_edit_message(self, before, after):
        if after.author.bot:
            return
        em = CustomEmbed(
            title="Messege Edit",
            description=f"**Bearbeitete Nachricht von**: {before.author}"
                        f"\r\n**Alte Nachricht**: {before.content}"
                        f"\r\n**Neue Nachricht**: {after.content}",
            timestamp=datetime.datetime.now())
        channel = await self.bot.fetch_channel(CHANID)

        if channel:
            await channel.send(file=self.bot.file, embed=em)

    @commands.Cog.listener("on_message_delete")
    async def log_deleted_message(self, message):
        if message.author.bot:
            return
        embed = CustomEmbed(
            title="Message Delete",
            description=f"**Gelöschte Nachricht von**: {message.author}"
                        f"\r\n**Inhalt der Nachricht**: {message.content}"
                        f"\r\n**Im Channel**: {message.channel.mention}",
            timestamp=datetime.datetime.now())

        if message.embeds:
            for i, embed_obj in enumerate(message.embeds, start=1):
                embed_title = f"Embed {i}" if len(message.embeds) > 1 else "Embed"

                embed_text = embed_obj.description if embed_obj.description else ""

                embed.add_field(name=f"--- {embed_title} ---", value=embed_text)

        channel = await self.bot.fetch_channel(CHANID)

        if channel:
            await channel.send(file=self.bot.file, embed=embed)


async def setup(bot):
    await bot.add_cog(Log(bot))