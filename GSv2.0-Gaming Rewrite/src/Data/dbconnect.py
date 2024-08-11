import aiosqlite
from typing import Optional, Literal

async def connect_execute(database, query: str, injectiontuple: Optional[tuple]=None, datatype: Optional[Literal["All", "One"]]=None):
	async with aiosqlite.connect(database) as conn:
		async with conn.execute(query, injectiontuple if injectiontuple is not None else None) as cur:
			if datatype == "All":
				return await cur.fetchall()
			elif datatype == "One":
				return await cur.fetchone()
			else:
				 await conn.commit()
				 
class ModmailBlacklist:
    db = "Data/team.db"

    @classmethod
    async def get_blacklist(cls, user_id=None, type: Literal["One", "All"]="One"):
        if type == "One":
            return await connect_execute(cls.db, "SELECT user_id FROM blacklist WHERE user_id = ?", (user_id,), datatype="One")
        if type == "All":
            return await connect_execute(cls.db, "SELECT user_id FROM blacklist", datatype="All")

    @classmethod
    async def add_blacklist(cls, user_id):
        await connect_execute(cls.db, "INSERT INTO blacklist (user_id) VALUES (?)", (user_id,))

    @classmethod
    async def remove_blacklist(cls, user_id):
        await connect_execute(cls.db, "DELETE FROM blacklist WHERE user_id = ?", (user_id,))