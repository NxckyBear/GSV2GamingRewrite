from discord.ext import commands
from discord import app_commands
import discord
import asyncio

from ...libs.bot import GSV2Bot
from ...libs.embeds import CustomEmbed
from ...view.team.ticket import ApplicationView, TicketView

class ApplicationCog(commands.Cog):
    def __init__(self, bot: GSV2Bot):
        self.bot = bot
        self.bot.add_view(TicketView())
        self.bot.add_view(ApplicationView())
        
    @app_commands.command(description='sende den bewerbungstext')
    @app_commands.checks.has_permissions(administrator=True)
    async def apptextsend(self, interaction: discord.Interaction):
        
        em = CustomEmbed(
            title=f'{interaction.guild.name} | Tickets',
            description='Willkommen im Support, Klicke unten und wähle ein Thema für Support\nIch hoffe das Support dir bei deinem Anliegen helfen kann')
        em.set_thumbnail(url=f"{interaction.guild.icon}")
        await interaction.respond('Ticket Message wurde gesendet', ephemeral=True)

        channel = self.bot.get_channel(1073702332082172084)
        await channel.send(file=self.bot.file, embed=em, view=ApplicationView())

    @app_commands.command(description='sende die Ticket Nachricht')
    @app_commands.checks.has_permissions(administrator=True)
    async def tickets(self, interaction: discord.Interaction):
        em = CustomEmbed(
            title=f'{interaction.guild.name} | Tickets',
            description='Willkommen im Support, Klicke unten und wähle ein Thema für Support\nIch hoffe das Support dir bei deinem Anliegen helfen kann',
            color=discord.Color.dark_gold()
        )
        em.set_thumbnail(url=f"{interaction.guild.icon}")
        em.set_image(url='https://cdn.discordapp.com/attachments/1073711669731151904/1216637088611696690/1666017515339-Yz02aFUJGDLIsbeaKtOUhf1E.png?ex=66011c95&is=65eea795&hm=105c903b16fca8586a7b432feeb8753c7168ebc2a412aceaedbae9b08fa487fb&')
        await interaction.response.send_message('Ticket Message wurde gesendet', ephemeral=True)

        channel = self.bot.get_channel(1073700885886152837)  # füge die Channel ID ein, wo die Ticket Nachricht mit dem Dropdown Menu geschickt werden soll
        await channel.send(embed=em, view=TicketView(), file=self.bot.file)


async def setup(bot):
    await bot.add_cog(ApplicationCog(bot))