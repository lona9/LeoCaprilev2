import discord
from discord import app_commands
from discord.ext import commands
from ..db import db
import pendulum
import datetime
from datetime import datetime
from apscheduler.triggers.cron import CronTrigger
from discord.ext import tasks
from datetime import timedelta
from discord.utils import get
import random
import pandas as pd

class tareas(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name = "t",
    description = "Agrega una tarea.")
    async def tarea(self, ctx: commands.Context, time: str, *, text) -> None:
        pass


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(tareas(bot))
