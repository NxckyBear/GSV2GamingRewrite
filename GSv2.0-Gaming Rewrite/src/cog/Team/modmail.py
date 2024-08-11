import discord, re
from discord.ext import commands
from ...Data.dbconnect import connect_execute
from ...libs.bot import GSV2Bot
from ...libs.embeds import CustomEmbed
from ...Data.dbconnect import ModmailBlacklist
from ...view.team.modmail import ModmailTicketView


class ModmailCog(commands.Cog):
    def __init__(self, bot: GSV2Bot) -> None:
        self.bot = bot
        self.bot.add_view(ModmailTicketView())

    async def on_message(self, message: discord.Message):
        category_id = 1216835850961162310
        teamping = '<@&1216835597017153677>'
        if message.author.bot:
            return
        if isinstance(message.channel, discord.DMChannel) and not await self.has_ticket(message.author.id):
            if await ModmailBlacklist.get_blacklist(message.author.id) is not None:
                embed = CustomEmbed(title='<:nope:1073700944941957291> | Blocked', description='Du bist blockiert und kannst kein Ticket erstellen!')
                await message.channel.send(file=self.bot.file, embed=embed)
                return
            if message.attachments or message.content:
                guild = self.bot.get_guild(1038267876622221332)
                category = guild.get_channel(category_id)
                channel = await category.create_text_channel(f"ticket-{message.author.name}")

                await connect_execute(self.bot.tdb, "INSERT INTO tickets (user_id, channel_id) VALUES (?, ?)", (message.author.id, channel.id))

            embed = CustomEmbed(title="WILLKOMMEN IM TICKET-SUPPORT!",
                                description="Ich habe deine Support-Anfrage erstellt und das Server-Team über dein Anliegen informiert.", color=discord.Color.green())

            team_embed = CustomEmbed(title="Neues Ticket!",
                                    description=f"Neues Ticket von: {message.author.mention}.")
            await message.channel.send(file=self.bot.file, embed=embed)
            await channel.send(teamping)
            await channel.send(file=self.bot.file, embed=team_embed, view=ModmailTicketView())

        if isinstance(message.channel, discord.DMChannel) and await self.has_ticket(message.author.id):
            row = await connect_execute(self.bot.tdb, "SELECT channel_id FROM tickets WHERE user_id = ?", (message.author.id,), datatype="One")

            if row:
                channel = self.bot.get_channel(row[0])

                embed = discord.Embed(description=f"{message.content}", color=discord.Color.green())
                embed.set_author(name=message.author,
                                url=message.author.jump_url,
                                icon_url=message.author.avatar.url)

                if message.attachments:
                    embed.set_image(url=message.attachments[0].url)

                await channel.send(embed=embed)
                await message.add_reaction("<:yes:1073716074140414013>")


        elif message.channel.category_id == category_id and not isinstance(message.channel, discord.DMChannel):
            row = await connect_execute(self.bot.tdb, "SELECT user_id FROM tickets WHERE channel_id = ?", (message.channel.id,), datatype="One")
            if row:
                user_id = row[0]
                user = self.bot.get_user(user_id)
                if user is None:
                    user = await self.bot.fetch_user(user_id)
                member = message.guild.get_member(message.author.id)
                ignore_roles = []

                highest_role = next((role for role in sorted(member.roles, key=lambda role: role.position, reverse=True) if
                                    role.name not in ignore_roles), None)
                if highest_role is None:
                    print("All roles are in the ignore_roles list.")
                else:
                    embedt = CustomEmbed(description=f"{message.content}\n")
                    embedt.set_author(name=f"{message.author} | {self.remove_emojis(highest_role.name)}",
                                    url=message.author.jump_url,
                                    icon_url=message.author.avatar.url)
                    if message.attachments:
                        embedt.set_image(url=message.attachments[0].url)
                    await user.send(file=self.bot.file, embed=embedt)
                    await message.add_reaction("<:yes:1073716074140414013>")
            await self.bot.process_commands(message)

    def remove_emojis(self, string):
        emoji_pattern = re.compile("["
                                u"\U0001F451-\U0001F4BB"
                                u"\U0001F334"
                                u"\U0001F4DA"
                                u"\U0001F4DD"
                                "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', string)

    async def has_ticket(self, user_id):
        row = await connect_execute(self.bot.tdb, "SELECT * FROM tickets WHERE user_id = ?", (user_id,), datatype="One")
        return bool(row)
#emoji = ("📝")
#unicode_codepoint = hex(ord(emoji))
#print(unicode_codepoint)

async def setup(bot):
    await bot.add_cog(ModmailCog(bot))