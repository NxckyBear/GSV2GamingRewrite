import discord, sys, traceback, aiosqlite, pyfiglet
from discord.app_commands.tree import CommandTree
from discord import app_commands
from discord.ext import commands

from ..cog.Community import CEXTENSIONS
from ..cog.Team import TEXTENSIONS
from .embeds import FailEmbed

class GSV2BotTree(CommandTree):
	async def on_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError, /) -> None:
		if isinstance(error, app_commands.CheckFailure):
			if isinstance(error, app_commands.MissingAnyRole):
				mrlist = "\n".join(error.missing_roles)
				embed = FailEmbed(description=f"dir fehlen folgeende rollen:\n\n{mrlist}")
				interaction.response.send_message(embed=embed, ephemeral=True)
			if isinstance(error, app_commands.MissingRole):
				embed = FailEmbed(description=f"dir fehlen folgeende rolle:\n\n{error.missing_role}")
				interaction.response.send_message(embed=embed, ephemeral=True)
			if isinstance(error, app_commands.MissingPermissions):
				embed = FailEmbed(f"dir fehlen folgende berechtigungen:\n\n{'\n'.join(error.missing_permissions)}")
				interaction.response.send_message(embed=embed, ephemeral=True)

		else:
			print(f"Exception raised in appcommand {interaction.command.name}:" if interaction.command else "Exception raised in View:")
			traceback.print_exception(type(error), error, error.__traceback__, limit=None, file=sys.stderr)

class GSV2Bot(commands.Bot):
	TOKEN = "DEIN TOKEN"
	tdb = "Data/team.db"
	cdb = "Data/community.db"
	def __init__(self) -> None:
		super().__init__("/", tree_cls=GSV2BotTree(), intents=discord.Intents.all())

	async def setup_hook(self):
		pyfiglet.print_figlet('GSV 2')
		self.file = discord.File("libs/GSv_Logo_ai.png", filename='GSv_Logo.png')
		for extension in CEXTENSIONS:
			await self.load_extension(extension)
			print(f'Load module: {extension.split(".")[3]}')
		for extension in TEXTENSIONS:
			await self.load_extension(extension)
			print(f'Load team_module: {extension.split(".")[3]}')
		async with aiosqlite.connect(self.cdb) as conn:
			await conn.execute("CREATE TABLE IF NOT EXISTS voice_channels (user_id INTEGER PRIMARY KEY, channel_id INTEGER NOT NULL)")
			await conn.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, msg_count INTEGER DEFAULT 0, voice_count INTEGER DEFAULT 0, xp INTEGER DEFAULT 0)")
			await conn.execute('CREATE TABLE IF NOT EXISTS counting (guild_id INTEGER PRIMARY KEY, last_number INTEGER, last_user_id INTEGER)')
		async with aiosqlite.connect(self.tdb) as conn:
			await conn.execute('CREATE TABLE IF NOT EXISTS team_members (user_id INTEGER PRIMARY KEY, message_count INTEGER, strikes INTEGER)')
			await conn.execute('CREATE TABLE IF NOT EXISTS message_history (user_id INTEGER, date TEXT, message_count INTEGER)')
			await conn.execute('CREATE TABLE IF NOT EXISTS goal_history (user_id INTEGER, week_start TEXT, goal_reached TEXT)')
			await conn.execute('CREATE TABLE IF NOT EXISTS servers (uid INTEGER PRIMARY KEY, reason TEXT, mod_id INTEGER)''')
			await conn.execute("CREATE TABLE IF NOT EXISTS WarnList (warn_id INTEGER PRIMARY KEY, mod_id INTEGER, guild_id INTEGER, user_id INTEGER, warns INTEGER DEFAULT 0, warn_reason TEXT, warn_time TEXT)""")
			await conn.execute("CREATE TABLE IF NOT EXISTS blacklist(user_id INTEGER PRIMARY KEY)")
			await conn.execute('CREATE TABLE IF NOT EXISTS abmeldung (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, grund TEXT, start_date TEXT, end_date TEXT)')

		