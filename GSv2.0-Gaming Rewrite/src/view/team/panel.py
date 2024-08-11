import discord, asyncio, datetime
from discord.ext import commands
from discord.ext.commands.cooldowns import CooldownMapping
from ...Data.dbconnect import connect_execute
from ...libs.embeds import *

class KnastMenu(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Besucherrollenantrag", style=discord.ButtonStyle.primary)
    async def besuch_Button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = CustomEmbed(
            title="✔ | Anfrage Erfolgreich!",
            description=f"{interaction.user.mention} deine Anfrage wurde an das team geschickt!",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

        embed = CustomEmbed(
            title="🚨 | Neue Anfrage",
            description=f"{interaction.user.mention} möchte die besucher rolle haben!",
            color=discord.Color.red()
        )
        self.disable_all_buttons()
        channel = interaction.guild.get_channel(1251558364635332689) # Replace with your channel ID
        if channel:
            await channel.send(embed=embed, view=BesuchButton(interaction.user, 1184593699523526696), file=interaction.client.file)

    @discord.ui.button(label="Entlassungsantrag", style=discord.ButtonStyle.primary)
    async def entlassung_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = CustomEmbed(
            title="✔ | Anfrage Erfolgreich!",
            description=f"{interaction.user.mention} deine Anfrage wurde an das team geschickt!",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

        embed = CustomEmbed(
            title="🚨 | Neue Anfrage",
            description=f"{interaction.user.mention} möchte Entlassen werden!",
            color=discord.Color.red()
        )
        self.disable_all_buttons()
        channel = interaction.guild.get_channel(1251558364635332689) # Replace with your channel ID
        if channel:
            await channel.send(embed=embed, view=EntlassungButton(interaction.user, 1184593699523526696), file=interaction.client.file)

    def disable_all_buttons(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True

class BesuchButton(discord.ui.View):
    def __init__(self, user, role):
        super().__init__()
        self.user = user
        self.role = role

    async def interaction_check(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("Du hast nicht die erforderlichen Berechtigungen!", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Annehmen", style=discord.ButtonStyle.success, custom_id="besuchen_button", emoji="✔")
    async def besuchen(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.guild.get_member(self.user.id) 
        role = interaction.guild.get_role(1184550310451101697)
        if member and role:
            await member.add_roles(role)
            try:
                await self.user.send("Deine Anfrage für die Entlassung wurde akzeptiert.")
            except discord.Forbidden:
                pass
            embed = CustomEmbed(
                title="Anfrage",
                description=f"{self.user.mention} hat eine Anfrage geschickt und wurde akzeptiert."
            )
            self.disable_all_buttons()
            await interaction.message.edit(view=self)
            await interaction.response.send_message(embed=embed, ephemeral=True, file=interaction.client.file)
            self.start_removal_task(member, role)

    @discord.ui.button(label="Ablehnen", style=discord.ButtonStyle.red, custom_id="ablehnen_button", emoji="❌")
    async def ablehnen(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await self.user.send("Deine Anfrage für die Besucherrolle wurde abgelehnt.")
        except discord.Forbidden:
            pass
        embed = CustomEmbed(
            title="Anfrage",
            description=f"{self.user.mention} hat eine Anfrage geschickt und wurde abgelehnt."
        )
        self.disable_all_buttons()
        await interaction.message.edit(view=self)
        await interaction.response.send_message(embed=embed, ephemeral=True, file=interaction.client.file)

    def disable_all_buttons(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True

    def start_removal_task(self, member, role):
        async def remove_role_after_delay():
            await asyncio.sleep(1800)  # 30 minutes in seconds
            await member.remove_roles(role)
            try:
                await member.send(f"Deine Besucherrolle wurde entfernt nach 30 Minuten.")
            except discord.Forbidden:
                pass

        asyncio.create_task(remove_role_after_delay())

class EntlassungButton(discord.ui.View):
    def __init__(self, user, role):
        super().__init__()
        self.user = user
        self.role = role

    async def interaction_check(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("Du hast nicht die erforderlichen Berechtigungen!", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Annehmen", style=discord.ButtonStyle.success, custom_id="entlassung_annehmen", emoji="✔")
    async def annehmen(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.guild.get_member(self.user.id)
        role = interaction.guild.get_role(1184593699523526696)
        if member and role:
            try:
                await member.remove_roles(role)
                await self.user.send("Deine Anfrage für die Entlassung wurde akzeptiert.")
            except discord.Forbidden:
                pass

            embed = CustomEmbed(
                title="Anfrage akzeptiert",
                description=f"{self.user.mention} wurde aus dem Knast entlassen."
            )
            self.disable_all_buttons()
            await interaction.message.edit(view=self)
            await interaction.response.send_message(embed=embed, ephemeral=True, file=interaction.client.file)

    @discord.ui.button(label="Ablehnen", style=discord.ButtonStyle.danger, custom_id="entlassung_ablehnen", emoji="❌")
    async def ablehnen(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await self.user.send("Deine Anfrage für die Entlassung wurde abgelehnt.")
        except discord.Forbidden:
            pass

        embed = CustomEmbed(
            title="Anfrage abgelehnt",
            description=f"{self.user.mention} wurde nicht aus dem Knast entlassen."
        )
        self.disable_all_buttons()
        await interaction.message.edit(view=self)
        await interaction.response.send_message(embed=embed, ephemeral=True, file=interaction.client.file)

    def disable_all_buttons(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True

class AdminView(discord.ui.View):
    def __init__(self, member, reason):
        super().__init__()
        self.member = member
        self.reason = reason
        self.db_path = "Data/team.db"
        self.knast_role_id = 1184593699523526696
        self.cooldown = CooldownMapping.from_cooldown(1, 300, commands.BucketType.member)

    @discord.ui.button(label="Warn", emoji="🚧")
    async def warn_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        warn_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await connect_execute(self.db_path, "INSERT INTO WarnList (user_id, guild_id, warns, warn_reason, mod_id, warn_time) VALUES (?, ?, ?, ?, ?, ?)", (self.member.id, interaction.guild.id, 1, self.reason, interaction.user.id, warn_time))
        row = await connect_execute(self.db_path, "SELECT warn_id FROM WarnList WHERE user_id = ? AND guild_id = ? ORDER BY warn_id DESC LIMIT 1", (self.member.id, interaction.guild.id), datatype="One")
        warn_id = row[0]

        warnUser_embed = CustomEmbed(
            title="`⚠️` Warn",
            description=f"Du wurdest auf dem Server **{interaction.guild.name}** verwarnt.",
            timestamp=datetime.datetime.now())
        warnUser_embed.add_field(name="Moderator:", value=f"```{interaction.user.name}```", inline=False)
        warnUser_embed.add_field(name="Warn ID:", value=f"```{warn_id}```", inline=False)
        warnUser_embed.add_field(name="Grund:", value=f"```{self.reason}```", inline=False)
        warnUser_embed.set_author(name=f"{interaction.guild.name}", icon_url=self.member.avatar.url)
        warnUser_embed.set_thumbnail(url=self.member.avatar.url)

        warn_embed = CustomEmbed(
            title="`✅` Warn",
            description=f"Du hast den User {self.member.mention} auf dem Server **{interaction.guild.name}** gewarnt.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now())
        warn_embed.add_field(name="Moderator:", value=f"```{interaction.user.name}```", inline=False)
        warn_embed.add_field(name="Warn ID:", value=f"```{warn_id}```", inline=False)
        warn_embed.add_field(name="Grund:", value=f"```{self.reason}```", inline=False)
        warn_embed.set_author(name=f"{interaction.guild.name}", icon_url=interaction.user.avatar.url)
        warn_embed.set_thumbnail(url=self.member.avatar.url)

        await self.member.send(file=interaction.client.file, embed=warnUser_embed)
        await self.interaction.response.send_message(file=interaction.client.file, embed=warn_embed, ephemeral=False)

    @discord.ui.button(label="Warnings", style=discord.ButtonStyle.primary)
    async def warnings_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        warns_info = []
        rows = await connect_execute(self.db_path, "SELECT warn_id, mod_id, warn_reason, warn_time FROM WarnList WHERE user_id = ? AND guild_id = ?", (self.member.id, interaction.guild.id), datatype="All")
        for row in rows:
            warn_id, mod_id, warn_reason, warn_time = row
            warn_time = datetime.datetime.strptime(warn_time, '%Y-%m-%d %H:%M:%S')
            warns_info.append((f"**Warn-ID:** __{warn_id}__ | **Warn ausgestellt am:** {warn_time.strftime('%Y-%m-%d %H:%M:%S')}", f"**Moderator:** <@{mod_id}> | **Mod-ID**: __{mod_id}__", f"**> Grund:**\n```{warn_reason}```"))

        warnings_embed = CustomEmbed(title=f"`⚠️` Warn Liste {self.member.name}")
        warnings_embed.set_author(name=f"{interaction.guild.name}", icon_url=interaction.guild.icon.url)
        warnings_embed.set_thumbnail(url=self.member.avatar.url)

        if warns_info == []:
            warnings_embed.description = f"The user has no warns!"
            warnings_embed.color = discord.Color.red()

        else:
            warnings_embed.description = "__**Liste der Warns**__"

            [warnings_embed.add_field(name=f"{warntime}", value=f"{mod}\n{reason}", inline=False) for warntime, mod, reason in warns_info]
        
        await interaction.response.send_message(file=interaction.client.file, embed=warnings_embed, ephemeral=False)

    @discord.ui.button(label="Unwarn", emoji="🍀")
    async def unwarn_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        warn_id = None  # Define warn_id variable
        row = await connect_execute(self.db_path, "SELECT warn_id FROM WarnList WHERE user_id = ? AND guild_id = ? ORDER BY warn_id DESC LIMIT 1", (self.member.id, interaction.guild.id), datatype="One")
        warn_id = row[0]
        await connect_execute(self.db_path, "DELETE FROM WarnList WHERE user_id = ? AND guild_id = ? AND warn_id = ?",(self.member.id, interaction.guild.id, warn_id))

        unwarnUser_embed = CustomEmbed(
            title="`🍀` Unwarn",
            description=f"Ein Warn von dir vom Server **{interaction.guild.name}** wurde zurückgezogen.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now())
        unwarnUser_embed.add_field(name="Moderator:", value=f"```{interaction.user.name}```", inline=False)
        unwarnUser_embed.add_field(name="Warn ID:", value=f"```{warn_id}```", inline=False)
        unwarnUser_embed.add_field(name="Grund:", value=f"```{self.reason}```", inline=False)
        unwarnUser_embed.set_author(name=f"{interaction.guild.name}", icon_url=interaction.client.user.avatar.url)
        unwarnUser_embed.set_thumbnail(url=interaction.guild.icon.url)

        unwarn_embed = CustomEmbed(
            title=f"`✅` Unwarn",
            description=f"Du hast den {self.member.mention} aus dem Server **{interaction.guild.name}** unwarned.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now())
        unwarn_embed.add_field(name="Moderator:", value=f"```{interaction.user.name}```", inline=False)
        unwarn_embed.add_field(name="Warn ID:", value=f"```{warn_id}```", inline=False)
        unwarn_embed.add_field(name="Grund:", value=f"```{self.reason}```", inline=False)
        unwarn_embed.set_author(name=f"{interaction.guild.name}", icon_url=interaction.client.user.avatar.url)
        unwarn_embed.set_thumbnail(url=self.member.avatar.url)

        await self.member.send(file=interaction.client.file, embed=unwarnUser_embed)
        await interaction.response.send_message(file=interaction.client.file, embed=unwarn_embed, ephemeral=False)

    @discord.ui.button(label="Timeout", emoji="⌛", style=discord.ButtonStyle.secondary)
    async def timeout_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = FailEmbed()

        if self.member == interaction.guild.owner:
            embed.description = 'Der Owner kann nicht getimeouted werden'
        elif self.member == self.bot.user:
            embed.description = 'Ich kann nicht getimeouted werden'
        elif self.member == interaction.user:
            embed.description = 'Du kannst dich nicht selber timeouten'
        else:
            embed = CustomEmbed(title="", description=f'{self.member.mention} wurde getimeouted')
            try:
                membed = CustomEmbed(title="Getimeouted", description=f"Du wurdest im server {interaction.guild.name} getimeouted\nGrund: {self.reason}")
                await self.member.send(embed=membed, file=interaction.client.file)
            except:
                embed.description += "\n\nBenutzer konnte nicht angeschrieben werden"
                print("Geht net")
            await self.member.timeout_for(datetime.timedelta(minutes=5))

        await interaction.response.send_message(file=interaction.client.file, embed=embed, ephemeral=True)

    @discord.ui.button(label="Kick", emoji="🚫", style=discord.ButtonStyle.danger)
    async def kick_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = FailEmbed()
        
        if self.member == self.guild.owner:
            embed.description = 'Der Owner kann nicht gekickt werden'
        elif self.member == self.bot.user:
            embed.description = 'Ich kann mich nicht kicken'
        elif self.member == interaction.user:
            embed.description = 'Du kannst dich nicht selber kicken'
        else:
            embed = CustomEmbed(title="", description=f"{self.member.name} wurde von {interaction.guild.name} gekickt")
            try:
                membed = CustomEmbed(title="Gekickt", description=f"Du wurdest im server {interaction.guild.name} gekickt\nGrund: {self.reason}")
                await self.member.send(embed=membed, file=interaction.client.file)
            except:
                embed.description += "\n\nBenutzer konnte nicht angeschrieben werden"
                print("Geht net")
            await self.member.kick(reason=f"wurde von {interaction.user.name} übers Admin panel gekickt")

        await interaction.response.send_message(file=interaction.client.file, embed=embed, ephemeral=True)

    @discord.ui.button(label="Ban", emoji="🔨", style=discord.ButtonStyle.danger)
    async def ban_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = FailEmbed()
        
        if self.member == self.guild.owner:
            embed.description = 'Der Owner kann nicht gebannt werden!'
        elif self.member == self.bot.user:
            embed.description = 'Ich kann mich nicht bannen!'
        elif self.member == interaction.user:
            embed.description = 'Du kannst dich nicht selber bannen!'
        else:
            embed = CustomEmbed(title="", description=f"{self.member.name} wurde von {interaction.guild.name} gebannt")
            try:
                membed = CustomEmbed(title="Gebannt", description=f"Du wurdest im server {interaction.guild.name} gebannt\nGrund: {self.reason}")
                await self.member.send(embed=membed, file=interaction.client.file)
            except discord.Forbidden:
                embed.description += "\n\nBenutzer konnte nicht angeschrieben werden"
                print("Geht net")
            await self.member.ban(reason=f"wurde von {interaction.user.name} übers Admin panel gebannt")

        await interaction.response.send_message(file=interaction.client.file, embed=embed, ephemeral=True)
    
    @discord.ui.button(label="Knast", style=discord.ButtonStyle.danger)
    async def knast_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(self.knast_role_id)

        if role is None:
            await interaction.response.send_message("Die Knast-Rolle wurde nicht gefunden.", ephemeral=True)
            return

        embed = SuccessEmbed(
            description=f"{self.member.mention} wurde in den Knast gesteckt\n"
                        f"**weitere Informationen:**\n"
                        f"`👮‍♂️` **Moderator:** {interaction.user}\n"
                        f"`🚨` **Grund:** {self.reason}")

        try:
            await connect_execute(self.db_path, "INSERT INTO servers (uid, reason, mod_id) VALUES (?, ?, ?)", (self.member.id, self.reason, interaction.user.id))

            await self.member.add_roles(role)
            await interaction.response.send_message(embed=embed, ephemeral=True, file=interaction.client.file)
        except Exception as e:
            await interaction.response.send_message(f"Ein Fehler ist aufgetreten: {e}", ephemeral=True)

    @discord.ui.button(label="knastentlassen", style=discord.ButtonStyle.success)
    async def entlassung_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = SuccessEmbed(
            description="User wurde entlassen!\n\n"
                        "**Weitere infos:**\n"
                        f"`👮‍♂️` **Moderator:** {interaction.user.name}")
        try:
            await connect_execute(self.db_path, "DELETE FROM servers WHERE uid = ?", (self.member.id,))

            role = interaction.guild.get_role(self.knast_role_id)

            if role is None:
                await interaction.response.send_message("Die Knast-Rolle wurde nicht gefunden.", ephemeral=True)
                return

            await self.member.remove_roles(role)
            await interaction.response.send_message(embed=embed, ephemeral=True, file=interaction.client.file)
        except Exception as e:
            await interaction.response.send_message(f"Ein Fehler ist aufgetreten: {e}", ephemeral=True)