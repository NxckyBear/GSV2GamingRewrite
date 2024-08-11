from datetime import datetime, timedelta
import discord
from discord.ext import commands
from discord import app_commands

from ...libs.bot import GSV2Bot
from ...libs.embeds import CustomEmbed

class AntiSpam(commands.Cog):

    def __init__(self, bot: GSV2Bot):
        self.bot = bot

        self.anti_spam = commands.CooldownMapping.from_cooldown(5, 15, commands.BucketType.member)
        self.too_many_violations = commands.CooldownMapping.from_cooldown(4, 60, commands.BucketType.member)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if type(message.channel) is not discord.TextChannel or message.author.bot:
            return

        bucket = self.anti_spam.get_bucket(message)
        retry_after = bucket.update_rate_limit()

        if retry_after:

            await message.delete()
            embed = CustomEmbed(title='Nicht Spammen', description=f"{message.author.mention}, don't spam!")
            await message.channel.send(file=self.bot.file, embed=embed, delete_after=10)

            violations = self.too_many_violations.get_bucket(message)
            check = violations.update_rate_limit()

            if check:
                until = datetime.now() + timedelta(minutes=10)
                await message.author.timeout(until)
                try:
                    embed = CustomEmbed(title="Don't Spam", description='Spamme bitte nicht die Kanäle voll\nIch musste dich daher Timeouten\n\nUnd ich werde es wiedertun wenn du weitermachst')
                    await message.author.send(file=self.bot.file, embed=embed)
                except:
                    print(f"Konnte keine Nachricht an {message.author.name} senden")
                    return

class Massrole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Gibt allen Mitgliedern die ausgewählte Rolle")
    @app_commands.checks.has_permissions(administrator=True)
    async def massrole(self, interaction: discord.Interaction, role: discord.Role):
        for member in interaction.guild.members:
            try:
                await member.add_roles(role)
            except discord.HTTPException as e:
                print(f"Fehler beim Hinzufügen der Rolle zu {member}: {e}")
        await interaction.response.send_message(f"Rolle {role.name} wurde allen Mitgliedern hinzugefügt.")

async def setup(bot):
    await bot.add_cog(Massrole(bot))
    await bot.add_cog(AntiSpam(bot))
