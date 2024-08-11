import discord
from ...libs.embeds import CustomEmbed

class HelpdeskView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(label="Community Manager", value="cm"),
        discord.SelectOption(label="Teamleitung", value="tl"),
        discord.SelectOption(label="Moderator", value="mod"),
        discord.SelectOption(label='Supporter', value="supp", emoji='<:TA_Supporter:1075169298399633448>'),
        discord.SelectOption(label='Leave', value='leave', emoji='🚧')]

    @discord.ui.select(
        placeholder="Helpdesk",
        min_values=1,
        max_values=1,
        options=options,
        custom_id="Helpdesk")
    async def callback(self, select, interaction: discord.Interaction):
        selected_value = select.values[0]

        if selected_value == "cm":
            cm_embed = CustomEmbed(title='Community Manager',
                                     description='Informationen und Rechte des Community Managers...')
            await interaction.response.send_message(file=interaction.client.file, embed=cm_embed, ephemeral=True)

        elif selected_value == "tl":
            tl_embed = CustomEmbed(title='Teamleitung', description='Informationen und Rechte der Teamleitung...')
            await interaction.response.send_message(file=interaction.client.file, embed=tl_embed, ephemeral=True)

        elif selected_value == "mod":
            mod_embed = CustomEmbed(title='Moderator', description='Du hast Moderator gewählt.')
            await interaction.response.send_message(file=interaction.client.file, embed=mod_embed, ephemeral=True)

        elif selected_value == "supp":
            supp_embed = CustomEmbed(title='Supporter', description='Du hast Supporter gewählt.')
            await interaction.response.send_message(file=interaction.client.file, embed=supp_embed, ephemeral=True)

        elif selected_value == "leave":
            leave_embed = CustomEmbed(title='Leave', description='Du hast Leave gewählt.')
            await interaction.response.send_message(file=interaction.client.file, embed=leave_embed, ephemeral=True)