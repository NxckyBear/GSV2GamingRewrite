import asyncio
import datetime
import discord
from discord import app_commands
from discord.ext import commands, tasks

from ...Data.dbconnect import connect_execute
from ...libs.embeds import CustomEmbed
from ...libs.bot import GSV2Bot

class Team(commands.Cog):
    def __init__(self, bot: GSV2Bot):
        self.bot = bot

    async def start_loops(self):
        await self.bot.wait_until_ready()
        self.check_messages.start()

    async def cog_load(self):
        await self.start_loops()

    def seconds_until_saturday_noon(self):
        now = datetime.datetime.now()
        next_saturday = now + datetime.timedelta((5 - now.weekday() + 7) % 7)
        next_saturday_noon = next_saturday.replace(hour=12, minute=0, second=0, microsecond=0)
        seconds_until = (next_saturday_noon - now).total_seconds()
        if seconds_until < 0:
            seconds_until += 7 * 24 * 60 * 60
        return seconds_until

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.guild is None:
            return

        special_role = message.guild.get_role(1044557317947019264)
        if special_role in message.author.roles:
            date = datetime.date.today().isoformat()
            result = await connect_execute(self.bot.tdb, "SELECT * FROM message_history WHERE user_id = ? AND date = ?",
                                (message.author.id, date), datatype="One")
            if result:
                await connect_execute(self.bot.tdb,
                    "UPDATE message_history SET message_count = message_count + 1 WHERE user_id = ? AND date = ?",
                    (message.author.id, date))
            else:
                await connect_execute(self.bot.tdb, "INSERT INTO message_history VALUES (?, ?, ?)", (message.author.id, date, 1))

    @app_commands.command(description="Auswertung der Teammitglieder history")
    @app_commands.rename(user="benutzer")
    @app_commands.describe(user="Der User dessen history ausgewertet werden soll")
    async def history(self, interaction: discord.Interaction, user: discord.User):
        two_weeks_ago = (datetime.date.today() - datetime.timedelta(weeks=2)).isoformat()
        result = await connect_execute(self.bot.tdb, "SELECT SUM(message_count) FROM message_history WHERE user_id = ? AND date >= ?", (user.id, two_weeks_ago), datatype="One")
        if result is not None and result[0] is not None:
            total_messages = result[0]
            goal_reached = 'Ja' if total_messages >= 150 else 'Nein'
            embed = CustomEmbed(
                title="User Evaluation",
                description=f"User: {user.name}\nGesamtzahl der Nachrichten in den letzten zwei Wochen: {total_messages}\nDas Ziel ist erreicht: {goal_reached}",)

            embed.set_author(name=user.name, icon_url=user.avatar.url)
            await interaction.response.send_message(file=self.bot.file, embed=embed)
        else:
            await interaction.response.send_message("User not found or no messages in the last two weeks")

    @app_commands.command(description="Vorhersage, ob der Benutzer das Ziel bis Samstag erreicht")
    @app_commands.rename(user="benutzer")
    @app_commands.describe(user="Der User dessen Fortschritt vorhergesagt werden soll")
    async def progress(self, interaction: discord.Interaction, user: discord.User):
        today = datetime.date.today()
        next_saturday = today + datetime.timedelta((5 - today.weekday() + 7) % 7)
        days_until_saturday = (next_saturday - today).days

        results = await connect_execute(self.bot.tdb, "SELECT date, SUM(message_count) FROM message_history WHERE user_id = ? GROUP BY date", (user.id,), datatype="All")
        if results:
            total_messages = sum(message_count for date, message_count in results)
            total_days = len(results)
            average_messages_per_day = total_messages / total_days

            predicted_messages = average_messages_per_day * days_until_saturday
            goal_reached = 'Ja' if predicted_messages >= 150 else 'Nein'
            embed = CustomEmbed(
                title="User Prediction",
                description=f"User: {user.name}\nVoraussichtliche Gesamtzahl der Nachrichten bis Samstag: {predicted_messages}\nDas Ziel wird erreicht: {goal_reached}")
            embed.set_author(name=user.name, icon_url=user.avatar.url)
            await interaction.response.send_message(file=self.bot.file, embed=embed)
        else:
            await interaction.response.send_message("User not found or no messages in the history")

    @app_commands.command(description="Zeigt die History, ob der Benutzer das Ziel erreicht hat")
    @app_commands.describe(user="Der User dessen Zielerreichungshistory angezeigt werden soll")
    async def goal_history(self, interaction: discord.Interaction, user: discord.User):
        results = await connect_execute(self.bot.tdb, "SELECT week_start, goal_reached FROM goal_history WHERE user_id = ? ORDER BY week_start DESC", (user.id,), datatype="All")
        if results:
            description = f"User: {user.name}\n\n"
            for week_start, goal_reached in results:
                description += f"Woche beginnend am {week_start}: Ziel erreicht: {goal_reached}\n"
            embed = CustomEmbed(
                title="Goal Achievement History",
                description=description)
            embed.set_author(name=user.name, icon_url=user.avatar.url)
            await interaction.response.send_message(file=self.bot.file, embed=embed)
        else:
            await interaction.response.send_message("No goal achievement history found for this user")

    @tasks.loop(hours=7 * 24)
    async def check_messages(self):
        guild = self.bot.get_guild(913082943495344179)
        if guild is None:
            return
        
        teamroles = [guild.get_role(r) for r in [1052676334247219291, 997504163544039484, 997504036041412619, 914076712373989386, 1070336143373119593, 1243955774221193247, 1141717278845571082]]
        teamrole = guild.get_role(1044557317947019264)
        if teamrole is None:
            return
        evaluation_channel = self.bot.get_channel(1249347322534559877)

        for member in teamrole.members:
            result = await connect_execute(self.bot.tdb, "SELECT strikes FROM team_members WHERE user_id = ?", (member.id,), datatype="One")
            if result:
                strikes = result[0]
                user = member

                # Calculate message count for the week
                one_week_ago = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()
                week_result = await connect_execute(self.bot.tdb, "SELECT SUM(message_count) FROM message_history WHERE user_id = ? AND date >= ?",
                                    (member.id, one_week_ago), datatype="One")
                if week_result and week_result[0] is not None:
                    week_message_count = week_result[0]
                else:
                    week_message_count = 0

                # Check message count and update strikes
                if week_message_count >= 150:
                    if strikes != 0:
                        strikes -= 1
                        goal_reached = 'Ja'
                else:
                    strikes += 1
                    goal_reached = 'Nein'

                await connect_execute(self.bot.tdb, "UPDATE team_members SET message_count = 0, strikes = ? WHERE user_id = ?",
                                    (strikes, member.id,))
                await connect_execute(self.bot.tdb, "INSERT INTO goal_history VALUES (?, ?, ?)",
                                    (member.id, one_week_ago, goal_reached))
                embed = CustomEmbed(
                    title="User Evaluation",
                    description=f"User: {user.name}\nMessage Count: {week_message_count}\nStrikes: {strikes}")
                embed.set_author(name=user.name, icon_url=user.avatar.url)
                await evaluation_channel.send(file=self.bot.file, embed=embed)

                # Remove roles if strikes exceed the limit
                if strikes > 2:
                    for role in teamroles:
                        if role in member.roles:
                            await member.remove_roles(role)
                    await member.remove_roles(teamrole)
                    await connect_execute(self.bot.tdb, "DELETE FROM team_members WHERE user_id = ?", (member.id,))
            else:
                await connect_execute(self.bot.tdb, "INSERT INTO team_members VALUES (?, ?, ?)", (member.id, 0, 1))

    @check_messages.before_loop
    async def before_check_messages(self):
        await self.bot.wait_until_ready()
        seconds_until = self.seconds_until_saturday_noon()
        await asyncio.sleep(seconds_until)

async def setup(bot):
    await bot.add_cog(Team(bot))