from discord.ext import commands
import discord
from discord import app_commands
from ...libs.bot import GSV2Bot
from ...libs.embeds import SuccessEmbed, CustomEmbed
from ...view.team.helpdesk import HelpdeskView


class HelpdeskCog(commands.Cog):
    def __init__(self, bot: GSV2Bot):
        self.bot = bot
        self.bot.add_view(HelpdeskView())
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Helpdesk wurde geladen')

    @app_commands.command(description="Aktualisiere das Helpdesk menü")
    @app_commands.checks.has_permissions(administrator=True)
    async def helpdesk(self, interaction: discord.Interaction):
        channel = self.bot.get_channel(1120360814331838514)

        embed_successful = SuccessEmbed('Das Helpdesk wurde erfolgreich gesendet / aktualisiert')

        embed = CustomEmbed(
            title='<a:5006_i_support:1075166049785364543> | Helpdesk | <:TA_Supporter:1075169298399633448> ',
            description='Willkommen im Helpdesk von GSv\n'
                        'Hier wirst du über deine Aufgaben informiert, und ebenso die Möglichkeiten welche sich dir hier bieten\n'
                        'Wähle weiter unten einfach deine Rolle aus um mehr über sie und ihre Rechte zu erfahren\n\n'
                        'Das Helpdesk steht dir BTW Immer zur Verfügung\n'
                        'jz lass uns rocken\n'
                        '<:G_:1158950908613361694><:S_:1158950928586657802><:v_:1158950963009310770>')
        await interaction.response.send_message(file=self.bot.file, embed=embed_successful, ephemeral=True)
        await channel.send(file=self.bot.file, embed=embed, view=HelpdeskView())


async def setup(bot):
    await bot.add_cog(HelpdeskCog(bot))