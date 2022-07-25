import discord
from discord.ext import commands
from discord import app_commands
from ..db import db
from asyncio import sleep
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

COGS = ["reminders"]

class Ready(object):
  def __init__(self):
    for cog in COGS:
      setattr(self, cog, False)

  def ready_up(self, cog):
    setattr(self, cog, True)
    print(f" {cog} cog ready")

  def all_ready(self):
    return all([getattr(self, cog) for cog in COGS])

class MyBot(commands.Bot):

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        db.autosave(self.scheduler)

        self.ready = False

        super().__init__(
        command_prefix = '$',
        intents = discord.Intents.all(),
        application_id = 830893492694679602
        )

    async def setup_hook(self):
        for cog in COGS:
            await self.load_extension(f"lib.cogs.{cog}")
            print(f" {cog} cog loaded")

        print("setup complete")
        await bot.tree.sync()

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            raise

        else:

            self.log_channel = self.get_channel(830872167075938315)

            await self.log_channel.send("Ocurrió un error.")

            raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, discord.ext.commands.errors.CommandNotFound):
          pass

        elif hasattr(exc, "original"):
          raise exc

        else:
          raise exc

    async def on_ready(self):
        if not self.ready:

            log_channel = self.get_channel(830872167075938315)
            await log_channel.send('Estoy listo, estoy listo, estoy listo!')

            self.scheduler.start()

            self.ready = True

            stream = discord.Game("La Vega")
            await self.change_presence(status=discord.Status.online, activity=stream)
        else:
            print("leo caprile reconnected")

bot = MyBot()
