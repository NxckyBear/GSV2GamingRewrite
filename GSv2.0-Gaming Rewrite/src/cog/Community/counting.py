import discord
from discord.ext import commands

from ...libs.bot import GSV2Bot
from ...libs.embeds import CustomEmbed
from ...Data.dbconnect import connect_execute

class CountingCog(commands.Cog):
    def __init__(self, bot):
        self.channel_id = 1243269123379691662
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.channel.id != self.channel_id:
            return

        try:
            number = int(message.content)
        except ValueError:
            return

        try:
            await self.handle_counting(message, number)
        except Exception as e:
            print(f"An error occurred: {e}")

    async def handle_counting(self, message, number):
        row = await connect_execute(self.bot.cdb, 'SELECT last_number, last_user_id FROM counting WHERE guild_id = ?', (message.guild.id,), datatype="One")
        if row:
            last_number, last_user_id = row
            if last_number is None:
                await self.handle_first_counting(message, number)
            elif number == last_number + 1 and last_user_id != message.author.id:
                await self.handle_correct_counting(message, number)
            else:
                await self.handle_incorrect_counting(message, last_user_id)
        else:
            await self.handle_first_counting(message, number)

    async def handle_correct_counting(self, message, number):
        await message.add_reaction('<:yes:1073716074140414013>')
        await connect_execute(self.bot.cdb, 'UPDATE counting SET last_number = ?, last_user_id = ? WHERE guild_id = ?', (number, message.author.id, message.guild.id))
        if number % 100 == 0:
            await message.add_reaction('🔥')
            embed = CustomEmbed(title='Herzlichen Glückwunsch!', description=f'Ihr seid jetzt schon bei der Nummer: `{number}` 🎉. Weiter so!')
            await message.channel.send(file=self.bot.file, embed=embed, delete_after=120)

    async def handle_incorrect_counting(self, message, last_user_id):
        await message.add_reaction('<:nope:1073700944941957291>')
        row = await connect_execute(self.bot.cdb, 'SELECT last_number FROM counting WHERE guild_id = ?', (message.guild.id,), datatype="One")
        if row:
            last_number = row[0]
            if last_user_id == message.author.id:
                embed = CustomEmbed(title='<:nope:1073700944941957291> | Error', description=f'{message.author.mention} Du kannst nicht zweimal hintereinander zählen!\nDie nächste zahl ist 1')
                await message.channel.send(file=self.bot.file, embed=embed, delete_after=30)
                await message.delete()
            else:
                embed = CustomEmbed(title='<:nope:1073700944941957291> | Error', description=f'{message.author.mention} Du hast falsch gezählt, die nächste Zahl wäre `{last_number + 1}`.\nDie nächste zahl ist 1')
                await message.channel.send(file=self.bot.file, embed=embed, delete_after=30)
                await message.delete()
            await connect_execute(self.bot.cdb, "DELETE FROM counting WHERE last_user_id = ?", (last_user_id,))

    async def handle_first_counting(self, message, number):
        await connect_execute(self.bot.cdb, 'INSERT OR REPLACE INTO counting (guild_id, last_number, last_user_id) VALUES (?, ?, ?)', (message.guild.id, number, message.author.id))
        await message.add_reaction('<:G_:1158950908613361694>')
        await message.add_reaction('<:S_:1158950928586657802>')
        await message.add_reaction('<:v_:1158950963009310770>')


async def setup(bot):
    await bot.add_cog(CountingCog(bot))
