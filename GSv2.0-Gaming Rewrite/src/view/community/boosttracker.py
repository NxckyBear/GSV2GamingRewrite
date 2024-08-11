import discord, asyncio
from discord.ui import View, Button

from ...libs.embeds import CustomEmbed

class GSVClanButtonView(View):
    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.button(label='join GSv clan', style=discord.ButtonStyle.blurple, custom_id='join')
    async def action_button_pressed(self, interaction: discord.Interaction, button: Button):
        embed = CustomEmbed(title='<a:party_blob:1073701093101551676> Willkommen im GSv clan', description='Du hast damit nun viele coole Extra rechte auf dem Discord und Zugriff zu exklusiven channels\n'
                                                                                                           'wir wünschen viel spaß <3')
        await interaction.user.add_roles(1026556535909929040)
        asyncio.sleep(1)
        await interaction.response.send_message(file=interaction.client.file, embed=embed)