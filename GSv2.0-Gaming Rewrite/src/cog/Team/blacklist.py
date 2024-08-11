import discord
from discord.ext import commands
from discord import app_commands

from ...libs.embeds import *
from ...Data.dbconnect import ModmailBlacklist
from ...libs.bot import GSV2Bot


class ModmailBlacklistCog(commands.Cog):
    def __init__(self, bot: GSV2Bot):
        self.bot = bot

    blacklist = app_commands.Group("dm_support", description="Group of commands for managing modmail blacklisting", guild_only=True)

    @blacklist.command(name="ban", description="Sperre ein User")
    @app_commands.checks.has_permissions(administrator=True)
    async def ban(self, interaction: discord.Interaction, user: discord.User):
        if user.bot:
            await interaction.response.send_message("Du kannst keine Bots bannen!", ephemeral=True)
            return
        if await ModmailBlacklist.get_blacklist(user.id) is not None:
            embed = CustomEmbed(
                title="<:off:1238127750372524052> | User ist bereits gesperrt!",
                description="Dieser Benutzer ist bereits gesperrt!",
                color=discord.Color.red()
            )
        else:
            await ModmailBlacklist.add_blacklist(user.id)
            embed = CustomEmbed(
                title="<:verifybadge:1238127161978654822> | User wurde gesperrt!",
                description=f"{user.mention} wurde erfolgreich gesperrt!\n"
                            f"Der Benutzer kann keine tickets mehr erstellen!",
                color=discord.Color.red()
            )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @blacklist.command(description="Entsperre ein User")
    @app_commands.checks.has_permissions(administrator=True)
    async def unban(self, interaction: discord.Interaction, user: discord.User):
        if await ModmailBlacklist.get_blacklist(user.id) is None:
            embed = CustomEmbed(
                title="<:off:1238127750372524052> | User ist nicht gesperrt!",
                description="Dieser Benutzer ist nicht gesperrt!",
                color=discord.Color.red()
            )
        else:
            await ModmailBlacklist.remove_blacklist(user.id)
            embed = CustomEmbed(
                title="<:verifybadge:1238127161978654822> | User wurde entsperrt!",
                description=f"{user.mention} wurde erfolgreich entsperrt!",
                color=discord.Color.green()
            )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @blacklist.command(description="Zeige alle gesperrten User")
    @app_commands.checks.has_permissions(administrator=True)
    async def list(self, interaction):
        blacklist = await ModmailBlacklist.get_blacklist(type="All")
        if not blacklist:
            await interaction.send("Es sind keine Benutzer auf der Blacklist!")
            return
        blacklist = [f"<@{user_id}>" for user_id in blacklist]
        embed = discord.Embed(
            title="Blacklist",
            description=f"Die Blacklist enthält folgende Benutzer:\n{', '.join(blacklist)}",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModmailBlacklistCog(bot))
