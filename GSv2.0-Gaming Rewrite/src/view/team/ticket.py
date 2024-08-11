import discord, asyncio
from ...libs.embeds import CustomEmbed, FailEmbed

options = [
    discord.SelectOption(label='Allgemein Support', description='Allgemeiner Support für alle anderen Themen', emoji='📩', value='1'),
    discord.SelectOption(label='User Report', description='Wähle diese Option um eine Partnerschaft zu beantragen', emoji='💫', value='2'),
    discord.SelectOption(label='Coding Wünsche', description='Wähle diese Option wenn du einen Bug gefunden hast', emoji='👩‍💻', value='3')
]


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        min_values=1,
        max_values=1,
        placeholder='Wähle hier die Art des Tickets',
        options=options,
        custom_id='Ticket'
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        view = CloseButtonView()
        cat = interaction.client.get_channel(1073702320870793328) # füge die Categorie ID ein, wo die Tickets erstellt werden sollen
        try:
            ticket_channel = await interaction.guild.create_text_channel(f'ticket-{interaction.user.name}', category=cat, topic=f'Ticket by {interaction.user} \nUser-ID: {interaction.user.id}')
            await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True, view_channel=True)
            await ticket_channel.set_permissions(interaction.guild.default_role, view_channel=False)
            em1 = CustomEmbed(
                title='📬 Ticket open!',
                description=f'{interaction.user.mention}, Ich habe dein Ticket erstellt\nHier findest du es: {ticket_channel.mention}',
                color=discord.Color.green())
            await interaction.response.send_message(embed=em1, file=interaction.client.file, ephemeral=True)
            if select.values[0] == "1":
                em2 = CustomEmbed(
                    title=f'Willkommen in deinem Ticket, {interaction.user.name}',
                    description='*Möchtest du dieses schließen, verwende bitte den Button unten*\n\n\n'
                                '**Bevor wir starten hat das Team noch einige Fragen an dich**\n'
                                '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n'
                                '**↬** Wie können wir dir helfen\n'
                                '**↬** Was ist der Grund für die Ticket eröffnung\n'
                                '**↬** bei beantworteten Fragen wird sich ein Teammitglied sehr gerne um dich kümmern\n'
                                '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬',
                    color=discord.Color.green())
            if select.values[0] == "2":
                em2 = CustomEmbed(
                    title=f'Willkommen in deinem Ticket, {interaction.user.name}',
                    description='*Möchtest du dieses schließen, verwende bitte den Button unten*\n\n\n'
                                '**Bevor wir starten hat das Team noch einige Fragen an dich**\n'
                                '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n'
                                '**↬** Gründe warum du eine Partnerschaft möchest\n'
                                '**↬** Anzahl der User deines Servers\n'
                                '**↬** Link zu deinem Server\n'
                                '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬',
                    color=discord.Color.green())

            if select.values[0] == "3":
                em2 = discord.Embed(
                    title=f'Willkommen in deinem Ticket, {interaction.user.name}',
                    description='*Möchtest du dieses schließen, verwende bitte den Button unten*\n\n\n'
                                '**Bevor wir starten hat das Team noch einige Fragen an dich**\n'
                                '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n'
                                '**↬** Welchen Bug möchtest du reporten\n'
                                '**↬** Was für auswirkungen hat dieser auf den Server?\n'
                                '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬',
                    color=discord.Color.green()
                )
            teamping = '<@&1044557317947019264>'
            message = '<@&989913773898891365>\n<@&1104810262269284392>\n<@&1106948915783291001>\n<@&1106949164379672586>'
            await ticket_channel.send(teamping)
            await ticket_channel.send(embed=em2, view=view)
            await asyncio.sleep(0.1)
            await ticket_channel.send(message, delete_after=0.1)
        except Exception as e:
            emE = FailEmbed(f'{interaction.user.mention}, Leider konnte ich dein Ticket nicht erstellen\nMelde dies bitte: <@696282645100888086>')
            await interaction.response.send_message(embed=emE, file=interaction.client.file, ephemeral=True)
            print(e)

class ApplicationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Bewerben", style=discord.ButtonStyle.success,
        custom_id='button:Appbutton')
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:

            cat = interaction.guild.get_channel(1073702320870793328)  # füge die Categorie ID ein, wo die Tickets erstellt werden sollen

            ticket_channel = await interaction.guild.create_text_channel(f'ticket-{interaction.user.name}', category=cat,
                                                                            topic=f'Ticket by {interaction.user}\nUser-ID: {interaction.user.id}')
            await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True,
                                                    view_channel=True)
            await ticket_channel.set_permissions(interaction.guild.default_role, view_channel=False)
        
            em1 = CustomEmbed(
                title='📬 Ticket open!',
                description=f'{interaction.user.mention}, Ich habe dein Ticket erstellt\nHier findest du es: {ticket_channel.mention}',
                color=discord.Color.green())

            await interaction.response.send_message(file=interaction.client.file, embed=em1, ephemeral=True)
        except:
            em1E = FailEmbed(f'{interaction.user.mention}, Leider konnte ich dein Ticket nicht erstellen\nMelde dies bitte: <@696282645100888086>')
            await interaction.response.send_message(file=interaction.client.file, embed=em1E, ephemeral=True)

        try:
            teamping = '<@&1044557317947019264>'
            message = '<@&989913773898891365>\n<@&1104810262269284392>\n<@&1106948915783291001>\n<@&1106949164379672586>'
            em2 = CustomEmbed(
                title=f'Willkommen in deinem Bewerbungsgespräch, {interaction.user.name}',
                description='*Möchtest du dieses schließen, verwende bitte den Button unten*\n\n\n'
                            '**Bevor wir starten hat das Team noch einige Fragen an dich**\n'
                            '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n'
                            '**↬** auf welche stelle möchtest du dich bewerben?\n'
                            '**↬** warum sollten wir dich nehmen\n'
                            '**↬** was erwartest du von uns\n'
                            '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬')
            await ticket_channel.send(teamping)
            await ticket_channel.send(file=interaction.client.file, embed=em2, view=CloseButtonView())
            await asyncio.sleep(0.1)
            await ticket_channel.send(message, delete_after=0.1)
        except:
            em2E = FailEmbed(f'{interaction.user.mention}, Leider konnte ich dein Ticket nicht erstellen\nMelde dies bitte: <@696282645100888086>')
            await ticket_channel.send(embed=em2E, file=interaction.client.file)

class CloseButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Close Ticket', style=discord.ButtonStyle.red, custom_id='Button:Close')
    async def closebutton(self, interaction: discord.Interaction, button: discord.ui.Button):
        closeticket = CustomEmbed(
            title="GSV Ticket System",
            description="Dein Ticket wird in 3 Sekunden geschlossen und der Kanal gelöscht",
            color=discord.Color.red())
        
        ticketclosed = CustomEmbed(
            title=f"GSV Ticket System",
            description=f"{interaction.user.mention}, Dein Ticket auf **{interaction.guild.name}** wurde geschlossen!\n",
            color=0xffffff)
        ticketclosed.add_field(name="\nDas könnten die Gründe sein:",
                                value="**↬** Du hast nicht mehr geantwortet\n**↬** Deine Support anfrage wurde erfolreich bearbeitet\n\n**✺ Wenn du weitere Hilfe brauchst zögere nicht in <#1073700885886152837> ein weiteres Ticket zu eröffnen ✺**\n",
                                inline=False)
        ticketclosed.add_field(name="Ticket Owner", value=f"{interaction.user.mention}", inline=True)
        ticketclosed.add_field(name="Ticket Name", value=f"{interaction.channel.name}", inline=True)
        ticketclosed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1073711669731151904/1107462738692816956/tenor.gif")

        await interaction.response.send_message(embed=closeticket, file=interaction.client.file)
        await asyncio.sleep(3)
        await interaction.channel.delete()
        await interaction.user.send(embed=ticketclosed, file=interaction.client.file)