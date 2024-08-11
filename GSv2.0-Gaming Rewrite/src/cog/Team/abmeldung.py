import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from ...Data.dbconnect import connect_execute
from ...libs.bot import GSV2Bot
from ...libs.embeds import CustomEmbed, SuccessEmbed

class LOACog(commands.Cog):
    def __init__(self, bot: GSV2Bot):
        self.bot = bot
        self.dbp = self.bot.tdb


    @app_commands.command(name="abmelden", description="Melde dich für einen bestimmten Zeitraum ab")
    @app_commands.describe(grund="Grund für die Abwesenheit", start_date="Startdatum der Abwesenheit (DD.MM.YYYY)", end_date="Enddatum der Abwesenheit (DD.MM.YYYY)")
    @app_commands.rename(start_date="start datum", end_date="end datum")
    @app_commands.checks.has_role(1044557317947019264)
    async def abmelden(self, interaction: discord.Interaction, grund: str, start_date: str, end_date: str):
        try:
            start_date_obj = datetime.strptime(start_date, '%d.%m.%Y')
            end_date_obj = datetime.strptime(end_date, '%d.%m.%Y')
        except ValueError:
            await interaction.response.send_message("Bitte gebe ein gültiges Datum im Format DD.MM.YYYY an.", ephemeral=True)
            return

        now = datetime.now()
        if start_date_obj < now or end_date_obj < now:
            await interaction.response.send_message("Die angegebenen Daten müssen in der Zukunft liegen.", ephemeral=True)
            return

        if end_date_obj <= start_date_obj:
            await interaction.response.send_message("Das Enddatum muss nach dem Startdatum liegen.", ephemeral=True)
            return

        start_date_iso = start_date_obj.isoformat()
        end_date_iso = end_date_obj.isoformat()

        await connect_execute(self.dbp, '''INSERT INTO abmeldung (user_id, grund, start_date, end_date)
                                   VALUES (?, ?, ?, ?)''', (interaction.user.id, grund, start_date_iso, end_date_iso))

        embed = SuccessEmbed(
            description="Deine Abwesenheitsinformationen wurden erfasst und das Team informiert.\n"
                        f"**Grund:** {grund}\n"
                        f"**Beginn der Abwesenheit:** <t:{int(start_date_obj.timestamp())}:R>\n"
                        f"**Ende der Abwesenheit:** <t:{int(end_date_obj.timestamp())}:R>")

        await interaction.response.send_message(embed=embed, file=self.bot.file, ephemeral=True)

        channel = interaction.guild.get_channel(1172557019358703646)

        embed = CustomEmbed(
            title=f"✅ {interaction.user.name}s Abmeldung",
            description="Die folgenden Informationen wurden erfasst:\n"
                        f"**Grund:** {grund}\n"
                        f"**Beginn der Abwesenheit:** <t:{int(start_date_obj.timestamp())}:R>\n"
                        f"**Ende der Abwesenheit:** <t:{int(end_date_obj.timestamp())}:R>",
            color=discord.Color.green())
        if channel:
            await channel.send(embed=embed, file=self.bot.file)

    @app_commands.command(description="Zeige alle deine Abmeldungen an")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(user="Wähle einen Member")
    async def loalist(self, interaction: discord.Interaction, user: discord.User):

        abmeldungen = await connect_execute(self.dbp, '''SELECT grund, start_date, end_date FROM abmeldung WHERE user_id = ?''', (user.id,), datatype="All")
        if not abmeldungen:
            await interaction.response.send_message(f"{user.mention} hat keine Abmeldungen.", ephemeral=True)
            return

        embed = CustomEmbed(
            title=f"📋 {user.name}'s Abmeldungen",
            description=""
        )

        [
            embed.add_field(
                name=f"Abmeldung vom {datetime.fromisoformat(start_date).strftime('%d.%m.%Y')} bis {datetime.fromisoformat(end_date).strftime('%d.%m.%Y')}", 
                value=f"**Grund:** {grund}\n**Beginn der Abwesenheit:** <t:{int(datetime.fromisoformat(start_date).timestamp())}:R>\n**Ende der Abwesenheit:** <t:{int(datetime.fromisoformat(end_date).timestamp())}:R>",
                inline=False
            ) 
            for grund, start_date, end_date in abmeldungen]

        await interaction.response.send_message(embed=embed, file=self.bot.file, ephemeral=True)



async def setup(bot):
    await bot.add_cog(LOACog(bot))