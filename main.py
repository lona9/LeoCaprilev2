from lib.bot import bot

with open('.env', 'r', encoding='utf-8') as f:
    token = f.read()

bot.run(token)
