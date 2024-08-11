import discord, asyncio
from ...Data.dbconnect import connect_execute, ModmailBlacklist
from ...libs.embeds import CustomEmbed

class Ticketweiterleitung(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    options = [
        discord.SelectOption(
            label="Admin Weiterleitung",
            description="Leite das Ticket an einen Admin weiter",
            value="admin"),
        discord.SelectOption(
            label="Developer Weiterleitung",
            description="Leite das Ticket an einen Developer weiter",
            value="developer"),
        discord.SelectOption(
            label="Moderator Weiterleitung",
            description="Leite das Ticket an einen Moderator weiter",
            value="moderator"),
        discord.SelectOption(
            label="Management Weiterleitung",
            description="Leite das Ticket an das Management weiter",
            value="management")]

    @discord.ui.select(
        min_values=1,
        max_values=1,
        placeholder="Was möchtest du tun?",
        options=options,
        custom_id="Select:Ticketweiterleitung")
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        user_id_tuple = await connect_execute(interaction.client.tdb, "SELECT user_id FROM tickets WHERE channel_id = ?", (interaction.channel.id,))
        user_id = user_id_tuple[0]
        user = interaction.client.get_user(user_id)
        if user is None:
            user = await interaction.client.fetch_user(user_id)
        if select.values[0] == "admin":
            embed = CustomEmbed(
                title="Ticket wurde an Admin weitergeleitet!",
                description=f"Ich habe dein Ticket an einen Admin weitergeleitet. Bitte habe etwas Geduld.")
            teamping = '<@&1216835574510522438>'
            await user.send(file=interaction.client.file, embed=embed)
            await interaction.message.channel.send(teamping)
            await interaction.response.send_message("Das Ticket wurde an einen Admin weitergeleitet!")


        if select.values[0] == "moderator":
            teamping = '<@&1216835586229534830>'
            embed = CustomEmbed(
                title="Ticket wurde an Moderator weitergeleitet!",
                description=f"Ich habe dein Ticket an einen Moderator weitergeleitet. Bitte habe etwas Geduld.")
            await user.send(file=interaction.client.file, embed=embed)
            await interaction.message.channel.send(teamping)
            await interaction.response.send_message("Das Ticket wurde an einen Moderator weitergeleitet!")

        if select.values[0] == "developer":
            teamping = '<@&1216835580982202460>'
            embed = CustomEmbed(
                title="Ticket wurde an Developer weitergeleitet!",
                description=f"Ich habe dein Ticket an einen Developer weitergeleitet. Bitte habe etwas Geduld.")
            await user.send(file=interaction.client.file, embed=embed)
            await interaction.message.channel.send(teamping)
            await interaction.response.send_message("Das Ticket wurde an einen Developer weitergeleitet!")

        if select.values[0] == "management":
            teamping = '<@&1216835578373607444>'
            embed = CustomEmbed(
                title="Ticket wurde an das Management weitergeleitet!",
                description=f"Ich habe dein Ticket an das Management weitergeleitet. Bitte habe etwas Geduld.")
            await user.send(file=interaction.client.file, embed=embed)
            await interaction.message.channel.send(teamping)
            await interaction.response.send_message("Das Ticket wurde an das Management weitergeleitet!")

class Ticketmenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    options = [
        discord.SelectOption(
            label="Ticket Schließen",
            description="Schließe das Ticket",
            value="close"),
        discord.SelectOption(
            label="Claim",
            description="Beanspruche das Ticket",
            value="claim"),
        discord.SelectOption(
            label="User Blockieren",
            description="Blockiere den User",
            value="block")]

    @discord.ui.select(
        min_values=1,
        max_values=1,
        placeholder="Was möchtest du tun?",
        options=options,
        custom_id="select")
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        user_id_tuple = await connect_execute(interaction.client.tdb, "SELECT user_id FROM tickets WHERE channel_id = ?", (interaction.channel.id,), datatype="One")
        if select.values[0] == "block":

            if user is None:
                user = await interaction.client.fetch_user(user_id)
            await ModmailBlacklist.add_blacklist(user_id)
            embed = CustomEmbed(
            title="Du wurdest ausgeschlossen!",
            description=f"Du wurdest von support ausgeschlossen!\n"
                        f"du kannst dich [hier](https://discord.gg/jb2bBFJDsC) entbannen lassen")
            await user.send(file=interaction.client.file, embed=embed)
            await interaction.response.send_message("Der User wurde blockiert!")
            await connect_execute(interaction.client.tdb, "DELETE FROM tickets WHERE channel_id = ?", (interaction.channel.id,))
            await asyncio.sleep(5)
            await interaction.message.channel.delete()

        if select.values[0] == "close":
            if user_id_tuple is None:
                await interaction.response.send_message("No matching ticket found.")
                return
            user_id = user_id_tuple[0]

            await connect_execute(interaction.client.tdb, "DELETE FROM tickets WHERE channel_id = ?", (interaction.channel.id,))

            user = interaction.client.get_user(user_id)
            if user is None:
                user = await interaction.client.fetch_user(user_id)

            await interaction.response.send_message("Ticket wird geschlossen!")
            embed = CustomEmbed(
                title="Ticket geschlossen!",
                description=f"Das Ticket wurde von {interaction.user.mention} geschlossen.",
                color=discord.Color.red())
            embed.set_author(name=f"{interaction.user}", icon_url=interaction.user.avatar.url)
            await user.send(file=interaction.client.file, embed=embed)
            await interaction.message.channel.delete()

        if select.values[0] == "claim":
            user_id = user_id_tuple[0]
            user = interaction.client.get_user(user_id)
            if user is None:
                user = await interaction.client.fetch_user(user_id)
            embed = CustomEmbed(
                title="Ticket wurde beansprucht!",
                description=f"Guten Tag ich bin {interaction.user.mention} und ich werde dir jetzt weiterhelfen!\n"
                            f"Wie kann ich dir helfen?")
            await user.send(file=interaction.client.file, embed=embed)
            await interaction.response.send_message("Das Ticket wurde beansprucht!")


class ModmailTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Weiterleitung", style=discord.ButtonStyle.success, emoji="🍪", custom_id="keks", row=2)
    async def button_callback1(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = CustomEmbed(
            title="Weiterleitung",
            description="Bitte wähle aus an wen du das Ticket weiterleiten möchtest!\n"
                        "Sollte kein passender Teamler online sein, schreibe bitte in das Ticket das keiner da ist!")
        await interaction.response.send_message(file=interaction.client.file, embed=embed, view=Ticketweiterleitung(), ephemeral=True)


    @discord.ui.button(label="Ticket Menü", style=discord.ButtonStyle.success, emoji="🍕", custom_id="pizza", row=1)
    async def button_callback2(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = False
        embed = CustomEmbed(
            title="Ticket Menü",
            description="Bitte wähle aus was du tun möchtest!\n"
                        "Ticket erst schließen wenn das Problem gelöst wurde!\n\n"
                        "Ticket beanspruchen wenn du das Ticket bearbeiten möchtest!\n"
                        "Sollte das Ticket bereits beansprucht sein, schreibt nur der zugeteilte Supporter in das Ticket!")
        await interaction.response.send_message(file=interaction.client.file, embed=embed, view=Ticketmenu(), ephemeral=True)