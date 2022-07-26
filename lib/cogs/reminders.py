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

class reminders(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.check_reminder.start()

    @commands.hybrid_command(name = "r",
    description = "Agrega un recordatorio.")
    async def reminder(self, ctx: commands.Context, time: str, *, text) -> None:
        time_conversion = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        raw_time = int("".join([x for x in time if x.isdigit()]))
        time_unit = time[-1]

        if not time_unit.isalpha():
            await ctx.send("Input inválido!")

        else:
            time_to_add = raw_time * time_conversion[time_unit]

            reminder_time = datetime.now() + timedelta(seconds=time_to_add)

            rm_id = random.randint(1, 10000)

            author = ctx.message.author.mention

            channel = ctx.channel.id

            db.execute("INSERT OR IGNORE INTO reminders (ReminderID, ReminderTime, ReminderText, ReminderAuthor, ReminderChannel) VALUES (?, ?, ?, ?, ?)", rm_id, reminder_time, text, author, channel)

            db.commit()

            await ctx.send(f"Te recordaré **{text}** en **{time}**.")

    @tasks.loop(seconds = 1)
    async def check_reminder(self):
        stored_reminders = db.column("SELECT ReminderID FROM reminders")

        if stored_reminders == ():
            self.check_reminder.stop()

        else:
            for reminder_id in stored_reminders:
                time_to_check = db.record("SELECT ReminderTime FROM reminders WHERE ReminderID = ?", reminder_id)

                time_to_check = pd.to_datetime(time_to_check)

                if time_to_check > datetime.now():
                    continue

                else:
                    remindertext, reminderauthor, reminderchannel = db.record("SELECT ReminderText, ReminderAuthor, ReminderChannel FROM reminders WHERE ReminderID = ?", reminder_id)

                    channel = self.bot.get_channel(int(reminderchannel))

                    await channel.send(f"{reminderauthor}: recuerda **{remindertext}**!")

                    db.execute("DELETE FROM reminders WHERE ReminderID = ?", reminder_id)

                    db.commit()

    @check_reminder.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(reminders(bot))
