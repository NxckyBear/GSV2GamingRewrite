import discord
from discord.ext import commands
from discord import app_commands
from typing import Literal, Optional

from ...libs.bot import GSV2Bot
from ...libs.embeds import CustomEmbed
from ...view.community.selfroles import *


class role(commands.Cog):
    def __init__(self, bot: GSV2Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(SelfrolesAgeView())
        self.bot.add_view(SelfrolesColorView())
        self.bot.add_view(SelfrolesExtraView())
        self.bot.add_view(SelfrolesGenderView())
        self.bot.add_view(SelfrolesPingView())
        self.bot.add_view(SelfrolesPlatformsView())
        self.bot.add_view(SelfrolesRelationshipView())
        self.bot.add_view(SelfrolesSexualityView())

    @app_commands.command(description="Schicke eine Event-Nachricht ab")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(text="Wähle einen Text aus", channel="Der Channel, in dem das Menü gesendet werden soll")
    async def selfrole(self, interaction: discord.Interaction, text: Literal["Sexualität", "Beziehungsstatus", "Geschlechtsauswahl", "Alter", "Extras", "Farbenauswahl", "Pingrollen", "Plattformen"], channel: Optional[discord.TextChannel]=None):

        if channel is None:
            channel = interaction.channel

        embed = CustomEmbed()
        if text == "Sexualität":
            embed.title = "Sexualität"
            embed.description = "Freiwillige Angabe\nWenn du nicht willst, musst du nicht."
            embed.set_image(url='https://cdn.discordapp.com/attachments/1073711672717488129/1224031717015420938/sexualitat.png')
            view = SelfrolesSexualityView()
            await interaction.response.send_message("Nachricht geschickt", ephemeral=True)
            await channel.send(file=self.bot.file, embed=embed, view=view)

        elif text == "Beziehungsstatus":
            embed.title = "Beziehungsstatus"
            embed.description = "Angaben sind freiwillig"
            embed.set_image(url='https://cdn.discordapp.com/attachments/1073711672717488129/1224031757754433657/beziehungsstatus.jpeg')
            view = SelfrolesRelationshipView()
            await interaction.response.send_message("Nachricht geschickt", ephemeral=True)
            await channel.send(file=self.bot.file, embed=embed, view=view)

        elif text == "Extras":
            embed.title = "Extras"
            embed.description = ""
            view = SelfrolesExtraView()
            await interaction.response.send_message("Nachricht geschickt", ephemeral=True)
            await channel.send(file=self.bot.file, embed=embed, view=view)

        elif text == "Geschlechtsauswahl":
            embed.title = "Geschlechtsauswahl"
            embed.description = "Angaben sind freiwillig"
            view = SelfrolesGenderView()
            await interaction.response.send_message("Nachricht geschickt", ephemeral=True)
            await channel.send(file=self.bot.file, embed=embed, view=view)

        elif text == "Alter":
            embed.title = "Alter"
            embed.description = "Gebe hier dein Alter an"
            embed.set_image(url='https://cdn.discordapp.com/attachments/1073711672717488129/1224031776511623188/Alter.jpeg')
            view = SelfrolesAgeView()
            await interaction.response.send_message("Nachricht geschickt", ephemeral=True)
            await channel.send(file=self.bot.file, embed=embed, view=view)

        elif text == "Farbenauswahl":
            embed.title = "Farbenauswahl"
            embed.description = "Wähle unten im Menü die Rolle aus"
            embed.set_image(url='https://cdn.discordapp.com/attachments/1073711672717488129/1224031796535099462/Farbenauswahl.jpeg')
            view = SelfrolesColorView()
            await interaction.response.send_message("Nachricht geschickt", ephemeral=True)
            await channel.send(file=self.bot.file, embed=embed, view=view)

        elif text == "Pingrollen":
            embed.title="Pingrollen"
            embed.description=("Drücke [hier](https://discord.com/channels/913082943495344179/1073993336890871848/1249873609091190868), "
                                "um zum anfang der Selfroles zu gelangen")
            view = SelfrolesPingView()
            await interaction.response.send_message("Nachricht geschickt", ephemeral=True)
            await channel.send(file=self.bot.file, embed=embed, view=view)

        elif text == "Plattformen":
            embed.title = "Plattformen"
            embed.description = 'Wähle deine Plattform bzw. Plattformen\n- Damit die anderen User Bescheid wissen, wie sie mit dir spielen können'
            embed.set_image(url='https://cdn.discordapp.com/attachments/1073711672717488129/1224031589357588500/Plattformen.png')
            view = SelfrolesPlatformsView()
            await interaction.response.send_message("Nachricht geschickt", ephemeral=True)
            await channel.send(file=self.bot.file, embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(role(bot))


