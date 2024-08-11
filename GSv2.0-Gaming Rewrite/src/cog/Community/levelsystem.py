import discord
from discord.ext import commands, tasks
import aiosqlite

from ...libs.bot import GSV2Bot
from ...Data.dbconnect import connect_execute
from ...libs.embeds import CustomEmbed

class LevelSystem(commands.Cog):
    def __init__(self, bot: GSV2Bot):
        self.bot = bot
        self.DB = self.bot.cdb

    @staticmethod
    def get_level(xp):
        lvl = 1
        amount = 100 # Werte zum Leveln angeben

        while True:
            xp -= amount
            if xp < 0:
                return lvl
            lvl += 1
            if lvl >= 5 and lvl <= 20:
                amount += 200
            elif lvl >= 20:
                amount += 400
            amount += 250

    async def check_user(self, user_id):
        await connect_execute(self.DB, "INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))

    async def get_xp(self, user_id):
        await self.check_user(user_id)
        result = await connect_execute(self.DB, "SELECT xp FROM users WHERE user_id = ?", (user_id,), datatype="One")
        return result[0]

    async def get_msgcount(self, user_id):
        await self.check_user(user_id)
        result = await connect_execute(self.DB, "SELECT msg_count FROM users WHERE user_id = ?", (user_id,), datatype="One")
        return result[0]

    async def get_voicecount(self, user_id):
        await self.check_user(user_id)
        result = await connect_execute(self.DB, "SELECT voice_count FROM users WHERE user_id = ?", (user_id,), datatype="One")
        return result[0]

    @commands.Cog.listener()
    async def on_message(self, message):
        global lvlup
        if message.author.bot:
            return
        if not message.guild:
            return
        xp = 10

        await self.check_user(message.author.id)
        await connect_execute(self.DB, "UPDATE users SET msg_count = msg_count + 1, xp = xp + ? WHERE user_id = ?", (xp, message.author.id))

        new_xp = await self.get_xp(message.author.id)
        old_level = self.get_level(new_xp - xp)
        new_level = self.get_level(new_xp)
        msgcount = await self.get_msgcount(message.author.id)
        voicecount = await self.get_voicecount(message.author.id)
        if old_level == new_level:
            return

        rolledazu = "nein"
        role_map = {
            5: 1017133827631611954,
            10: 1051796133317464074,
            20: 1249354197770440724,
            35: 1249354328444244020,
            50: 1017134812802322503,
            75: 1032672722007904346,
            100: 1032673100409606204
        }

        if new_level in role_map:
            lvl = message.guild.get_role(role_map[new_level])
            await message.author.add_roles(lvl)
            rolledazu = "ja"

        if rolledazu == "ja":
            description = f"Herzlichen Glückwunsch <@{message.author.id}> du bist jetzt **Level {new_level}!**\n \n Du hast insgesamt **{msgcount} Nachrichten** geschrieben!\n Du hast die Rolle `{lvl}` freigeschaltet!"
            if voicecount != 0:
                description += f"\n Du hast insgesamt **{msgcount} Nachrichten** geschrieben und {voicecount} Minuten im Voice verbracht!"
        else:
            description = f"Herzlichen Glückwunsch <@{message.author.id}> du bist jetzt **Level {new_level}!** \nDu hast insgesamt **{msgcount} Nachrichten** geschrieben!"
            if voicecount != 0:
                description += f" und {voicecount} Minuten im Voice verbracht!"

        lvlup = CustomEmbed(
            title="Level up!",
            description=description)

        ch = message.author.dm_channel
        if ch is None:
            try:
                ch = await message.author.create_dm()
                await ch.send(file=self.bot.file, embed=lvlup)
            except discord.HTTPException:
                await message.channel.send(message.author.mention, file=self.bot.file, embed=lvlup, delete_after=400)
                print("Kann keine Nachricht an diesen Benutzer senden.")
                return
            

class VoiceLeveling(commands.Cog):
    def __init__(self, bot: GSV2Bot):
        self.bot = bot
        self.DB = self.bot.cdb

    @staticmethod
    def get_level(xp):
        lvl = 1
        amount = 10

        while True:
            xp -= amount
            if xp < 0:
                return lvl
            lvl += 1
            amount += 300

    async def check_user(self, user_id):
        await connect_execute(self.DB, "INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))

    async def get_xp(self, user_id):
        await self.check_user(user_id)
        result = await connect_execute(self.DB, "SELECT xp FROM users WHERE user_id = ?", (user_id,), datatype="One")
        return result[0]

    async def get_msgcount(self, user_id):
        await self.check_user(user_id)
        result = await connect_execute(self.DB, "SELECT msg_count FROM users WHERE user_id = ?", (user_id,), datatype="One")
        return result[0]

    async def get_voicecount(self, user_id):
        await self.check_user(user_id)
        result = await connect_execute(self.DB, "SELECT voice_count FROM users WHERE user_id = ?", (user_id,), datatype="One")
        return result[0]

    @commands.Cog.listener()
    async def on_ready(self):
        self.is_connected.start()

    @tasks.loop(minutes=1)
    async def is_connected(self):
        global lvlup, lvl
        xp = 10
        guild = self.bot.get_guild(913082943495344179)  # Server-ID

        radio_channels = [self.bot.get_channel(channel_id) for channel_id in [1076577676271304724, 1216646094776438814, 1073701146998350006, 1073701338157961216]]

        for member in guild.members:
            if member.voice:
                if member.voice.channel in radio_channels:
                    pass

                if len(member.voice.channel.voice_states.keys()) >= 2:

                    await connect_execute(self.DB, "UPDATE users SET voice_count = voice_count + 1, xp = xp + ? WHERE user_id = ?", (xp, member.id))
                    new_xp = await self.get_xp(member.id)
                    old_level = self.get_level(new_xp - xp)
                    new_level = self.get_level(new_xp)
                    voicecount = await self.get_voicecount(member.id)
                    msgcount = await self.get_msgcount(member.id)
                    if old_level == new_level:
                        pass
                    else:
                        role_map = {
                            5: 1017133827631611954,
                            10: 1051796133317464074,
                            20: 1249354197770440724,
                            35: 1249354328444244020,
                            50: 1017134812802322503,
                            75: 1032672722007904346,
                            100: 1032673100409606204
                        }

                        if new_level in role_map:
                            lvl = guild.get_role(role_map[new_level])
                            await member.add_roles(lvl)
                            rolledazu = "ja"
                        else:
                            rolledazu = "nein"
                            lvlup = CustomEmbed(
                                title="Level up!",
                                description=f"Herzlichen Glückwunsch <@{member.id}> du bist jetzt **Level {new_level}!** \nDu "
                                            f"warst insgesamt **{voicecount}** Minuten im Voice!")


                            if msgcount != 0:
                                lvlup = CustomEmbed(
                                    title="Level up!",
                                    description=f"Herzlichen Glückwunsch <@{member.id}> du bist jetzt **Level {new_level}!** \nDu "
                                                f"warst insgesamt **{voicecount}** Minuten im Voice und hast **{msgcount}** Nachrichten geschrieben geschrieben!")

                        if rolledazu == "ja":
                            lvlup = CustomEmbed(
                                title="Level up!",
                                description=f"Herzlichen Glückwunsch <@{member.id}> du bist jetzt **Level {new_level}!**\n \nDu warst insgesamt **{voicecount}** Minuten im Voice!\n Du hast die Rolle `{lvl}` freigeschaltet!")
                            if msgcount != 0:
                                lvlup = CustomEmbed(
                                    title="Level up!",
                                    description=f"Herzlichen Glückwunsch <@{member.id}> du bist jetzt **Level {new_level}!**\n \nDu warst insgesamt **{voicecount}** Minuten im Voice und hast **{msgcount}** Nachrichten geschrieben!\n Du hast die Rolle `{lvl}` freigeschaltet!")
                        ch = member.dm_channel
                        if ch is None:
                            try:
                                ch = await member.create_dm()
                            except discord.HTTPException:
                                chat = guild.get_channel(1073701634863009933)
                                await chat.send(member.name, file=self.bot.file, embed=lvlup, delete_after=400)

async def setup(bot):
    await bot.add_cog(LevelSystem(bot))
    await bot.add_cog(VoiceLeveling(bot))