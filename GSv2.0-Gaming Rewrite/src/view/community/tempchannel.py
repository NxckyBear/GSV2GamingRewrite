import discord, asyncio
from ...Data.dbconnect import connect_execute

class TempchannelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def interaction_check(self, interaction: discord.Interaction[discord.Client]) -> bool:
        channel_info = await connect_execute(interaction.client.cdb, "SELECT * FROM voice_channels WHERE channel_id = ?", (interaction.message.channel.id,), datatype="One")

        if not channel_info or interaction.user.id != channel_info[0]:
            await interaction.response.send_message("Du bist nicht der Besitzer des Channels.", ephemeral=True)
            return False
        else: return True

    @discord.ui.button(style=discord.ButtonStyle.gray, label="Limitieren", emoji="👥")
    async def call1(self, interaction: discord.Interaction, button: discord.ui.Button):
       
        def check(message):
            return message.author == interaction.user and message.channel == interaction.channel

        await interaction.response.send_message("Bitte gib die gewünschte Benutzerlimitierung für deinen Kanal ein:", ephemeral=True)
        try:
            response = await interaction.client.wait_for('message', check=check, timeout=30)
            limit = int(response.content)
            if 0 < limit <= 99:
                voice_channel = interaction.message.channel
                await voice_channel.edit(user_limit=limit)
                await interaction.followup.send(f"Benutzerlimit des Kanals auf {limit} gesetzt.", ephemeral=True)
                await asyncio.sleep(1)
                await response.delete()
            else:
                await interaction.followup.send("Ungültige Eingabe. Bitte gib eine Zahl zwischen 1 und 99 ein.", ephemeral=True)
        except asyncio.TimeoutError:
            await interaction.followup.send("Zeitlimit überschritten. Bitte versuche es erneut.", ephemeral=True)
        except ValueError:
            await interaction.followup.send(
                "Ungültige Eingabe. Bitte gib eine Zahl zwischen 1 und 99 ein.", ephemeral=True)
            
    @discord.ui.button(style=discord.ButtonStyle.gray, label="Rename", emoji="✏")
    async def call2(self, interaction: discord.Interaction, button: discord.ui.Button):
        def check(message):
            return message.author == interaction.user and message.channel == interaction.channel

        await interaction.response.send_message("Bitte gib den neuen Namen für deinen Kanal ein:", ephemeral=True)
        try:
            response = await interaction.client.wait_for('message', check=check, timeout=30)
            new_name = response.content
            voice_channel = interaction.message.channel
            await voice_channel.edit(name=new_name)
            await interaction.followup.send(f"Kanal erfolgreich in `{new_name}` umbenannt.", ephemeral=True)
            await asyncio.sleep(1)
            await response.delete()
        except asyncio.TimeoutError:
            await interaction.followup.send("Zeitlimit überschritten. Bitte versuche es erneut.", ephemeral=True)

    @discord.ui.button(style=discord.ButtonStyle.gray, label="Sperren", emoji="🔒")
    async def call3(self, interaction: discord.Interaction, button: discord.ui.Button):
        voice_channel = interaction.message.channel
        await voice_channel.set_permissions(interaction.guild.default_role, view_channel=True, connect=False)
        await interaction.response.send_message("Der Kanal wurde gesperrt.", ephemeral=True)

    @discord.ui.button(style=discord.ButtonStyle.gray, label="Entsperren", emoji="🔓")
    async def call4(self, interaction: discord.Interaction, button: discord.ui.Button):
        voice_channel = interaction.message.channel
        await voice_channel.set_permissions(interaction.guild.default_role, connect=True)
        await interaction.response.send_message("Der Kanal wurde entsperrt.", ephemeral=True)

    @discord.ui.button(style=discord.ButtonStyle.gray, label="Bannen", emoji="🔨")
    async def call5(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Bitte gib die ID des Benutzers an, den du bannen möchtest:", ephemeral=True)
        try:
            response = await self.bot.wait_for('message', timeout=30)
            user_id = int(response.content)
            voice_channel = interaction.message.channel
            member = voice_channel.guild.get_member(user_id)
            if member:
                await member.move_to(None)
                await voice_channel.set_permissions(member, connect=False)
                await interaction.followup.send(
                    f"{member.mention} wurde aus dem Kanal gebannt und gesperrt.",
                    ephemeral=True)
                await asyncio.sleep(1)
                await response.delete()
            else:
                await interaction.followup.send("Benutzer nicht gefunden.", ephemeral=True)
        except asyncio.TimeoutError:
            await interaction.followup.send("Zeitlimit überschritten. Bitte versuche es erneut.", ephemeral=True)

    @discord.ui.button(style=discord.ButtonStyle.gray, label="Kicken", emoji="⛔")
    async def call6(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Bitte gib die ID des Benutzers an, den du aus dem Kanal kicken möchtest:", ephemeral=True)
        try:
            response = await self.bot.wait_for('message', timeout=30)
            user_id = int(response.content)
            voice_channel = interaction.message.channel
            member = voice_channel.guild.get_member(user_id)
            if member:
                await member.move_to(None)
                await interaction.followup.send(
                    f"{member.mention} wurde aus dem Kanal gekickt.", ephemeral=True)
                await asyncio.sleep(3)
                await response.delete()
            else:
                await interaction.followup.send("Benutzer nicht gefunden.", ephemeral=True)
        except asyncio.TimeoutError:
            await interaction.followup.send("Zeitlimit überschritten. Bitte versuche es erneut.", ephemeral=True)

    @discord.ui.button(style=discord.ButtonStyle.gray, label="Eigentum-Übertragen", emoji="👑")
    async def call7(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel_id = interaction.message.channel.id
        channel_info = await connect_execute(interaction.client.cdb, "SELECT * FROM voice_channels WHERE channel_id = ?", (channel_id,), datatype="One")

        if not channel_info:
            await interaction.response.send_message("Der Voice Channel existiert nicht in der Datenbank.", ephemeral=True)
            return

        current_owner = interaction.guild.get_member(channel_info[0])

        if interaction.user.id == current_owner.id:
            if current_owner.voice is None or current_owner.voice.channel != interaction.channel:
                await interaction.response.send_message(
                    "Du musst im gleichen Voice Channel wie der aktuelle Besitzer sein, um das Eigentum zu übertragen.",
                    ephemeral=True)
                return

            await interaction.response.send_message(
                "Bitte gib die ID des Benutzers an, dem du das Eigentum übertragen möchtest:",
                ephemeral=True)
            try:
                response = await self.bot.wait_for('message', timeout=30)
                new_owner_id = int(response.content)
                new_owner = interaction.guild.get_member(new_owner_id)
                if new_owner:
                    await connect_execute(interaction.client.cdb, "UPDATE voice_channels SET user_id = ? WHERE channel_id = ?", (new_owner.id, channel_id))
                    await interaction.followup.send(f"{new_owner.mention} ist jetzt der neue Besitzer des Kanals.", ephemeral=True)
                    await asyncio.sleep(1)
                    await response.delete()
                else:
                    await interaction.followup.send("Benutzer nicht gefunden.", ephemeral=True)
            except asyncio.TimeoutError:
                await interaction.followup.send("Zeitlimit überschritten. Bitte versuche es erneut.", ephemeral=True)
            except ValueError:
                await interaction.followup.send("Ungültige Benutzer-ID. Bitte gib eine korrekte Benutzer-ID an.", ephemeral=True)
        else:
            if current_owner.voice is not None:
                await interaction.response.send_message("Der aktuelle Besitzer ist online im Voice Channel. Nur er kann das Eigentum übertragen.", ephemeral=True)
                return

            await connect_execute(interaction.client.cdb, "UPDATE voice_channels SET user_id = ? WHERE channel_id = ?", (interaction.user.id, channel_id))
            await interaction.response.send_message(f"{interaction.user.mention} ist jetzt der neue Besitzer des Kanals.", ephemeral=True)

    @discord.ui.button(style=discord.ButtonStyle.grey, label=f"Voice Channel Löschen.", emoji="🧨")
    async def call8(self, interaction: discord.Interaction, button: discord.ui.Button):
            channel_info = await connect_execute(interaction.client.cdb, "SELECT * FROM voice_channels WHERE channel_id = ?", (interaction.channel.id,), datatype="One")
            member = interaction.guild.get_member(channel_info[0])
            voice_channel = interaction.message.channel
            await connect_execute(interaction.client.cdb, "DELETE FROM voice_channels WHERE channel_id = ?", (voice_channel.id,))
            await voice_channel.delete()
            await asyncio.sleep(2)
            if member:
                await member.send("Dein Voice-Kanal wurde per Button gelöscht!")