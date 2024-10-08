import discord
from discord.ext import commands
from ...libs.bot import GSV2Bot
from ...libs.embeds import CustomEmbed

class Welcome(commands.Cog):
    def __init__(self, bot: GSV2Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Verify", url="https://discord.com/channels/913082943495344179/1176254800493555763"))
        view.add_item(discord.ui.Button(label="Main Projekt", url="https://discord.gg/ufEjGrbYWw"))

        embed = CustomEmbed(
            title="Willkommen",
            description=f"Hey {member.mention}, Willkommen auf dem Server!\n")
        embed.add_field(name="Hilfe", value="Eine Einführung findest du hier: <#1073700811143647232>")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1073711672717488129/1216626262207107103/GSV_verify.gif?ex=66011280&is=65ee9d80&hm=39fe6e5e75340beb22147915f7014b8cbfd7a33964227d623f27bcd603818872&")

        role_ids = [1216629193090007071, 1249360620680384532, 1014881097064132649, 1014881106018979870,
                    1248744094436687992, 1014881110695616673, 1017133211215745135, 1205647946503290930,
                    1072233630019113060, 1249360002171404288, 1014881114491461632,
                    1014881119990190122, 1014881120921321543]
        for role_id in role_ids:
            role = member.guild.get_role(role_id)
            if role:
                await member.add_roles(role)
            else:
                print(f"Rolle mit ID {role_id} nicht gefunden.")

        channel = await self.bot.fetch_channel(1073701634863009933)  # Channel ID vom Willkommenschat
        await channel.send(file=self.bot.file, embed=embed, view=view)
        print(f"{member} joined the Server")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        user = member.name
        try:
            dm_channel = await member.create_dm()

            re_embed = CustomEmbed(title='<:nope:1073700944941957291> | Goodbye ', description='Hey hey\nmich hast du save schon gesehen, Entschuldige das ich dich einfach so anschreibe\ndu hast unseren Gaming Server verlassen, unser Team interessiert sich persönlich dafür\nund wäre dir mehr als Dankbar wenn du hier ein Feedback hinterlässt\n<3\nhttps://discord.gg/xexvmgp6qu\n\nAnsonnsten nochmal SRY für die Störung und danke fürs lesen')
            await dm_channel.send(file=self.bot.file, embed=re_embed)
            print(f'DM erfolgreich an {user} gesendet')
        except discord.Forbidden:
            print(f'Konnte keine Direktnachricht an {user} senden.')

async def setup(bot):
    await bot.add_cog(Welcome(bot))