import discord, asyncio
from discord.ext import commands, tasks
from discord import app_commands
from typing import Literal
from ...libs.bot import GSV2Bot
from ...libs.embeds import CustomEmbed, FailEmbed

OPTIONS = ['Voice', 'Deathchat', 'Team', 'Admin']

class Special(commands.Cog):
    
    def __init__(self, bot: GSV2Bot):
        self.bot = bot

    @tasks.loop(seconds=30)
    async def status(self):
        while True:
            await self.bot.change_presence(activity=discord.Game('/help to see all commands'), status=discord.Status.dnd)
            await asyncio.sleep(15)
            await self.bot.change_presence(activity=discord.Game('Developed by gsv2.dev'), status=discord.Status.dnd)
            await asyncio.sleep(15)
    
    @status.before_loop
    async def before_status(self):
        await self.bot.wait_until_ready()

    @app_commands.command(description="Pings command with multiple options.")
    @app_commands.describe(option="Choose an option")
    async def pings(self, interaction: discord.Interaction, option: Literal['Voice', 'Deathchat', 'Team', 'Admin']):
        embed = CustomEmbed()
        if option == 'Deathchat':
            message = '<@&1014881120921321543>'
            embed.title = '💀| Deathchatping |🔔'
            embed.description = (f'{interaction.user.name} hat den ping ausgeführt\n'
                                    f'\n'
                                    f'Dieser ping ist abstellbar in den <#1073993336890871848>\n'
                                    f'PS wir nehmen uns das recht raus sollte dieser ping nix bringen, andere zu pingen\n'
                                    f'Hate etc wird schwerstens bestraft, (Keine Angst, wir sind Hard aber Fair)')
            await interaction.send(message)
            await interaction.response.send_message(file=self.bot.file, embed=self.embed)
        elif option == 'Team':
            if 1070336143373119593 not in [role.id for role in interaction.user.roles]:
                await self.send_error(interaction, '"Dies ist eine Teamfunktion, bewerbe dich gerne fürs Team unter: <#1073702332082172084>"')
                return

            message = '<@&1044557317947019264>'
            embed.title = '💀| Teamping |🔔'
            embed.description = f'{interaction.user.name} hat den ping ausgeführt'
            await interaction.send(message)
            await interaction.response.send_message(file=self.bot.file, embed=self.embed)
        elif option == 'Admin':
            if 1044557317947019264 not in [role.id for role in interaction.user.roles]:
                await self.send_error(interaction, "Dies ist eine Adminfunktion.")
                return

            message = '<@696282645100888086>'
            embed.title = '💀| Adminping |🔔'
            embed.description = f'{interaction.user.name} hat den ping ausgeführt'
            await interaction.send(message)
            await interaction.response.send_message(file=self.bot.file, embed=self.embed)
        elif option == 'Voice':
            message = '<@&1248706499539238956>'
            embed.title = '🔊| Voiceping |🔔'
            embed.description = (f'{interaction.user.name} hat den ping ausgeführt\n'
                                    'Wie es aussieht sucht da jemand nen call\n'
                                    'Hoffe wir finden schnell Leute die sich anschließen <3')
            await interaction.send(message)
            await interaction.response.send_message(file=self.bot.file, embed=self.embed)

    async def send_error(self, interaction: discord.Interaction, error_message: str):
        em = discord.Embed(title=' ❌| Error | ❌', description=error_message, color=discord.Color.red())
        em.set_footer(text=self.embed.footer.text, icon_url=self.embed.footer.icon_url)
        await interaction.send(file=self.bot.file, embed=em, delete_after=15)

    @app_commands.command(description='📝┃Sende die Liste der Server-Emojis')
    async def emojilist(self, interaction: discord.Interaction):
        embed = CustomEmbed(
            title='Emojis',
            description='')

        if len(interaction.guild.emojis) > 50:
            embed = FailEmbed('Anscheinend gibt es zu viele Emojis auf diesem Server :( \nIch bin dadurch leider etwas eingeschränkt')
        else:
            for emoji in interaction.guild.emojis:
                embed.description += f'{emoji} - `{emoji}`\n'
        await interaction.response.send_message(file=self.bot.file, embed=embed, delete_after=120)

    @app_commands.command(description='.')
    @app_commands.has_permissions(administrator=True)
    async def coming_soon(self, interaction: discord.Interaction):
        message2 = 'erfolgreich gesendet'
        message = '# Coming Soon <a:Loading:1073700976000782396>'
        await interaction.response.send_message(message2, ephemeral=True)
        await interaction.send(message)

async def setup(bot):
    await bot.add_cog(Special(bot))