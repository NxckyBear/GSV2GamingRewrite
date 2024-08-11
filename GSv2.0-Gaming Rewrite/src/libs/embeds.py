from datetime import datetime
from typing import Any, Literal
import discord
from discord import Embed

class CustomEmbed(Embed):
    def __init__(self, color: int | discord.Colour | None = 0x2596be, title: Any | None = None, url: Any | None = None, description: Any | None = None, timestamp: datetime | None = None):
        super().__init__(color=color, title=title, type="rich", url=url, description=description, timestamp=timestamp)
        self.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

class SuccessEmbed(Embed):
    def __init__(self, description: Any | None = None, ):
        super().__init__(colour=discord.Colour.green(), title="`✅` Erfolgreich!", type="rich", description=description)
        self.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

class FailEmbed(Embed):
    def __init__(self, description: Any | None = None):
        super().__init__(colour=discord.Colour.red(), title='❌ Error!', description=description)
        self.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")