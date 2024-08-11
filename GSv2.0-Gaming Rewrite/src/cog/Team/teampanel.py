import asyncio
import datetime
import sys
import traceback
from discord.ext.commands.cooldowns import CooldownMapping
import discord
from discord.ext import commands, tasks
from discord import app_commands
from discord import ButtonStyle
from ...Data.dbconnect import connect_execute
from ...libs.embeds import *
from ...libs.bot import GSV2Bot
from ...view.team.panel import KnastMenu, AdminView

class ModSystem(commands.Cog):
    def __init__(self, bot: GSV2Bot):
        self.bot = bot
        self.timeout_role_id = 1184593699523526696 
        self.knast_role_id = self.timeout_role_id
        self.db_path = self.bot.tdb

    @tasks.loop(minutes=10)
    async def knastlist(self):
        guild = self.bot.get_guild(913082943495344179)
        channel = guild.get_channel(1234567890123456789) # channel id für den channel wo die knastliste reinkommen soll
        users = await connect_execute(self.db_path, "SELECT uid, reason, mod_id FROM servers", datatype="All")
        knast_members = [(guild.get_member(user_id), reason, guild.get_member(mod_id)) for user_id, reason, mod_id in users if guild.get_member(user_id)]
        
        embed = discord.Embed(
            title="Benutzer im Knast",
            color=discord.Color.red()
        )
        if knast_members != []:
            if users <= 25:
                [embed.add_field(name=member.name, value=f"Grund: {reason}\n\nModerator: {mod.mention if mod else 'Unbekannt'}") for member, reason, mod in knast_members]
            else:
                embedcount = (int(len(users)/25)+1)
                embedlist = []
                rest = round(len(users)/embedcount)
                for i in range(embedcount):
                    if i == 1:
                        fembed = embed
                        [embed.add_field(name=member.name, value=f"Grund: {reason}\n\nModerator: {mod.mention if mod else 'Unbekannt'}") for member, reason, mod in knast_members[:rest]]
                        [knast_members.remove(a) for a in knast_members[:rest]]
                        embedlist.append(fembed)
                    else:
                        if len(knast_members) <= rest:
                            nembed = discord.Embed(title="", description="", color=embed.color)
                            [embed.add_field(name=member.name, value=f"Grund: {reason}\n\nModerator: {mod.mention if mod else 'Unbekannt'}") for member, reason, mod in knast_members]
                            embedlist.append(nembed)
                        else:
                            nembed = discord.Embed(title="", description="", color=embed.color)
                            [embed.add_field(name=member.name, value=f"Grund: {reason}\n\nModerator: {mod.mention if mod else 'Unbekannt'}") for member, reason, mod in knast_members[:rest]]
                            [knast_members.remove(a) for a in knast_members[:rest]]
                            embedlist.append(nembed)
        else:
            embed.description = "Es befinden sich keine Benutzer im Knast."
        try:
            message = await channel.fetch_message(2345678901234567890) # message id von der nachricht, die die liste beinhaltet
            if not embedlist:
                await message.edit(embed=embed)
            else:
                await message.edit(embeds=embedlist)
        except discord.NotFound:
            print("knastlist: nachricht gibts nich")

    async def cog_load(self):
        await self.create_database()
        if await self.bot.wait_until_ready():
            self.knastlist.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None or message.author.bot:
            return

        dm_keywords = [" dm ", " direct message ", " private message "]
        if any([keyword in message.content.lower() for keyword in dm_keywords]):
            row = await connect_execute(self.db_path, "SELECT warns FROM WarnList WHERE user_id = ? AND guild_id = ? ORDER BY warn_id DESC LIMIT 1", (message.author.id, message.guild.id), datatype="One")
            if row:
                warns = row[0] + 1
            else:
                warns = 1

                warn_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                await connect_execute(self.db_path, "INSERT INTO WarnList (user_id, guild_id, warns, warn_reason, mod_id, warn_time) VALUES (?, ?, ?, ?, ?, ?)", (message.author.id, message.guild.id, warns, "Mentioning DMs is not allowed", self.bot.user.id, warn_time))

            if warns <= 3:
                await message.channel.send(
                    f"{message.author.mention}, DMs are not allowed. Please use the server channels.")
            else:
                await message.channel.send(
                    f"{message.author.mention}, you have been warned multiple times about mentioning DMs. Further actions may be taken.")

    @app_commands.command(description='Manage User sofern sie scheiße bauen (lol)')
    @app_commands.checks.has_role(1044557317947019264)
    async def teampanel(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        squad = member.public_flags
        view = AdminView(member, reason)

        knastuser = await connect_execute(self.db_path, "SELECT uid FROM servers WHERE uid = ?", (member.id,), datatype="One")
        if knastuser:
            view.children[6].disabled = True
        else:
            view.children[7].disabled = True


        if squad.hypesquad_bravery:
            squad = "House of Bravery"
        elif squad.hypesquad_brilliance:
            squad = "House of Brilliance"
        elif squad.hypesquad_balance:
            squad = "House of Balance"
        else:
            squad = "None"

        embed = CustomEmbed(
            title=f"{member.name} | AdminPanel",
            description=(f"`👥 User Name` - {member.name} \n `🆔 User ID` - {member.id} \n `👥 Display/Server name` - {member.display_name} \n "
                         f"`⏰ Created At` - <t:{int(member.created_at.timestamp())}:R> \n `⏰ Joined At` - <t:{int(member.joined_at.timestamp())}:R> \n"
                         f"`🪪 Hypersquad` {squad} \n `📢 Mention` - {member.mention} \n `🔗 Avatar Url` - [Click Here]({member.display_avatar.url})"))
        embed.set_thumbnail(url=member.display_avatar.url)
        await interaction.response.send_message(file=self.bot.file, embed=embed, view=view, ephemeral=True)

    @app_commands.command(description="Lösche Nachrichten aus dem Channel")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(amount="Anzahl an Nachrichten (min. 1 | max. 100)")
    async def purge(self, interaction: discord.Interaction, amount: int):
        if amount > 100:
            error_embed = FailEmbed(description="`Ich kann nicht mehr als 100 Nachrichten löschen!`")
            error_embed.set_thumbnail(url=interaction.guild.icon.url)
            await interaction.response.send_message(file=self.bot.file, embed=error_embed, delete_after=6, ephemeral=True)
        else:
            deleted = await interaction.channel.purge(limit=amount)
            success_embed = SuccessEmbed(description=f"**{len(deleted)}** `Nachrichten gelöscht!`")
            success_embed.set_thumbnail(url=interaction.guild.icon.url)
            await interaction.response.send_message(file=self.bot.file, embed=success_embed, delete_after=10, ephemeral=True)

    @app_commands.command(description="Zeige alle Warns eines Users aus dem Server an")
    @app_commands.checks.has_role(1044557317947019264)
    async def warnings(self, interaction: discord.Interaction, member: discord.Member):
        warns_info = []
        rows = await connect_execute(self.db_path, "SELECT warn_id, mod_id, warn_reason, warn_time FROM WarnList WHERE user_id = ? AND guild_id = ?", (member.id, interaction.guild.id), datatype="All")
        for row in rows:
            warn_id, mod_id, warn_reason, warn_time = row
            warn_time = datetime.datetime.strptime(warn_time, '%Y-%m-%d %H:%M:%S')
            warns_info.append((f"**Warn-ID:** __{warn_id}__ | **Warn ausgestellt am:** {warn_time.strftime('%Y-%m-%d %H:%M:%S')}", f"**Moderator:** <@{mod_id}> | **Mod-ID**: __{mod_id}__", f"**> Grund:**\n```{warn_reason}```"))

        warnings_embed = CustomEmbed(title=f"`⚠️` Warn Liste {member.name}")
        warnings_embed.set_author(name=f"{interaction.guild.name}", icon_url=interaction.guild.icon.url)
        warnings_embed.set_thumbnail(url=member.avatar.url)

        if warns_info == []:
            warnings_embed.description = f"The user has no warns!"
            warnings_embed.color = discord.Color.red()

        else:
            warnings_embed.description = "__**Liste der Warns**__"

            [warnings_embed.add_field(name=f"{warntime}", value=f"{mod}\n{reason}", inline=False) for warntime, mod, reason in warns_info]
        
        await interaction.response.send_message(file=self.bot.file, embed=warnings_embed, ephemeral=False)

    @app_commands.command(description="Rufe das Knast Menü auf")
    async def knastmenu(self, interaction: discord.Interaction):
        embed = CustomEmbed(title="Knast Menü", description="Wähle hier aus was du machen möchtest", color=discord.Colour.random())
        await interaction.response.send_message(embed=embed, view=KnastMenu(), file=self.bot.file)
        

async def setup(bot):
    await bot.add_cog(ModSystem(bot))