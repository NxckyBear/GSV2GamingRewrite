import discord
from discord.ui import View, button, Button

from ...libs.embeds import CustomEmbed

class CustomView(View):
    def __init__(self, timeout=None):
        super().__init__(timeout=timeout)

    @button(label='Close', style=discord.ButtonStyle.red, custom_id='button_close')
    async def action_button_pressed(self, interaction: discord.Interaction, button: Button):
        embed_4 = CustomEmbed(title='', description='')
        if interaction.channel.permissions_for(interaction.user).manage_threads:
            embed_4.title = '⛔| Archiviert |⛔'
            embed_4.description = "Dieser Thread wurde von einem Teammitglied archiviert!"
            await interaction.response.send_message(file=interaction.client.file, embed=embed_4)
            await interaction.channel.archive()
        elif interaction.user.id == interaction.channel.owner_id:
            embed_4.title = '⭕| Archiviert |⭕'
            embed_4.description = "Dieser Thread wurde von dem Author archiviert!"
            await interaction.response.send_message(file=interaction.client.file, embed=embed_4)
            await interaction.channel.archive()
        else:
            embed_4.title = '❌| Error |❌'
            embed_4.description = "Dieser Button kann nur von dem Thread Inhaber oder einem Teammiglied genutzt werden!"
            await interaction.response.send_message(file=interaction.client.file, embed=embed_4, ephemeral=True)