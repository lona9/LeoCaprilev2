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

class buttonHandler(discord.ui.View):
    @discord.ui.button(label="Done!", style=discord.ButtonStyle.success, emoji="✅")
    async def done_button(self, interaction: discord.Interaction, button=discord.ui.Button):
        button.disabled = True
        await interaction.response.send_message(content = f"Task done!")
        #code where it sets the task as "done" based on the ID

class tareas(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="t", description="Add a task")
    async def tarea(self, interaction: discord.Interaction, text: str) -> None:
        view = buttonHandler()
        #sends the text input back, and adds button
        await interaction.response.send_message(text, view=view)

        #code where it saves the text to database with an ID, and status as "pending"


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(tareas(bot))
