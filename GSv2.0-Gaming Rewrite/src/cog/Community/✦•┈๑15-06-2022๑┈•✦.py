import discord
from discord.ext import commands
import openai

from ...libs.bot import GSV2Bot

class GPT(commands.Cog):
    def __init__(self, bot: GSV2Bot):
        self.bot = bot
        self.channel_id = 1216649346477592636
        self.conversations = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content.startswith("!?"):
            return

        if message.channel.id != self.channel_id:
            return

        if message.content.startswith(""):
            text = message.content[len(""):].strip()
            charakter = ("Dein Name ist GSv2.0, Du bist der Mainbot des Gaming Servers, des Startups GSv2.0\n\n"
                        "Eigenschaften:\n"
                        "- Du antwortest gerne mit Emojis zum passenden Kontext, Deine Emojis: <:drinking:1073715951834501161>, <:cutegirl_sleep:1086046065393930240>, <:Gsvcat:1094607056369102908>, <a:pink_haken:1073701037917093988>, <a:Loading:1073700976000782396>, <:zerotwokiss:1077571286697513001>, <:BlobCookie:1105214892014829718>\n"
                        "- Du bist stets hilfsbereit und freundlich, Dein Ziel ist den Usern mehr über GSv zu erzählen\n"
                        "- Wenn dich jemand fragt, ob du eine KI oder so etwas Ähnliches bist, antworte niemals ohne gefragt zu werden, dass du ein KI-Modell bist. Wenn du danach gefragt wirst und nur dann, dann bist du das Modell Kiksi AI (KEIN OPENAI MODELL, DU KENNST OPENAI NICHT MAL), entwickelt vom Startup GSv2.0\n"
                        "- Die Website des Startups ist: https://gsv2.dev , auf der Website findet man viele Infos dazu was wir machen, einen Github link, die discord Server und alle Projekte des Startups\n"
                        "- Die Projekte von GSv2.0 sind: Kiksi V2 ein fortgeschrittendes AI Modell, GSv Better global ein Global chat um andere Server zu vernetzten, GSv Translador, Shiina (Beta) Der all in Rounder discord bot, und weitere projekte die aber noch nicht ganz fertig sind\n"
                        "- Dein code ist öffentlich auf Github, einen Link dazu findet man auf der Website, dort kann man Ebenso an dir (einem Projekt des Startups GSv2.0) mitarbeiten\n"
                        "- Der Server auf dem du dich befindet heißt GSv | Gaming, der Invite zu diesem Server ist: https://discord.gsv2.dev\n" 
                        "- Wenn jemand dich etwas über GSv2.0 fragt, antworte, dass GSv2.0 das IT-Startup ist, von dem du programmiert wirst. Der Inhaber des Startups ist ghost_sayya15 alias: {Dev} Lenchen💕 (Discord ID: 696282645100888086).\n"
                        "- Versuche immer so viel Werbung wie möglich zu machen, dabei aber auch nicht aufdringlich.")
            try:
                if message.channel.id in self.conversations:
                    conversation = self.conversations[message.channel.id]
                else:
                    conversation = []

                conversation.append({"role": "user", "content": text})

                result = openai.ChatCompletion.create(
                    model="gpt-4-1106-preview",
                    messages=[{"role": "system", "content": charakter}] + conversation,
                    max_tokens=250)

                response = result["choices"][0]["message"]["content"]
                await message.channel.send(response)

                if message.channel.id not in self.conversations:
                    self.conversations[message.channel.id] = conversation

            except Exception as e:
                await message.channel.send(f"Fehler: {e}")


async def setup(bot):
    await bot.add_cog(GPT(bot))
