import asyncio
import discord
from discord.ext import commands
from discord.utils import format_dt
from discord import app_commands

from ...view.community.boosttracker import GSVClanButtonView
from ...libs.embeds import CustomEmbed, FailEmbed
from ...libs.bot import GSV2Bot


class Boosttime(commands.Cog):
    def __init__(self, bot: GSV2Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.premium_since is None and after.premium_since is not None:
            booster = after
            embed = CustomEmbed(title='', description=f'Vielen Dank, {booster.mention}, dass du den Server geboostet hast! Wir schätzen deine Unterstützung!')
            channel = self.bot.get_channel(1073701634863009933)

            if channel is not None:
                await channel.send(file=self.bot.file, embed=embed, view=GSVClanButtonView())
        if after.premium_since is None and before.premium_since is not None:
            gsvclanrole = after.guild.get_role(1026556535909929040)
            if gsvclanrole in after.roles:
                await after.remove_roles(gsvclanrole)

    @app_commands.command(name="boostzeit", description="🚀〢 Zeigt dir deine Boostzeit an!")
    @app_commands.rename(member="benutzer")
    @app_commands.describe(member="Wähle ein Server-Mitglied aus!")
    async def boostime(self, interaction: discord.Interaction, member: discord.Member=None):
        user = member or interaction.user
        boostzeit = user.premium_since
        embed = FailEmbed()
        if user.bot:
            embed.description = '**Bots können keine Server boosten!**' 
        if user not in interaction.guild.members:
            embed.description = '**Dieser User ist leider nicht in GSv2.0**'

        if boostzeit is None:
            embed.description = "**Dieser User ist kein GSV Booster**"
        else:
            boostzeit_formatted = format_dt(boostzeit, style="R")
            embed = CustomEmbed(title='', description=f"**`🚀` | {user.mention} hat das Server Boosting auf diesem Server {boostzeit_formatted} gestartet!**")
        await interaction.response.send_message(file=self.bot.file, embed=embed)

async def setup(bot):
    await bot.add_cog(Boosttime(bot))
