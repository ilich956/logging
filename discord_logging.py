import logging
import logging.config  
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests

load_dotenv()

WEATHER_URL = os.getenv('WEATHER_URL')
API = os.getenv('API')
TOKEN = os.getenv('TOKEN')
CITY = "Astana"

main_formatter = logging.Formatter(
    "%(levelname)s - %(message)s - %(asctime)s"
)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

url = WEATHER_URL + "appid=" + API + "&q=" + CITY
response = requests.get(url).json()
 
def celsius(kelvin):
    return round(kelvin - 273.15, 2)

class DiscordBotHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    async def emit(self, record: logging.LogRecord, message=None):
        log = self.format(record)
        if message:
            await message.channel.send(log)

@client.event
async def on_ready():
    logging.info('Bot is ready.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/weather'):
        kelvin = response['main']['temp']
        await message.channel.send(f'Weather in Astana: {celsius(kelvin)} celsius')
        logging.info('Weather info sent.')
        
        await discord_handler.emit(logging.LogRecord("logger", logging.INFO, "", 0, "Weather info sent.", (), None, None), message=message)

class Filter(logging.Filter):
    def filter(self, record):
        return not (record.msg.lower().startswith('bot'))

root_logger = logging.getLogger()

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(main_formatter)

file = logging.FileHandler(filename="logs.txt")
file.setLevel(logging.DEBUG)
file.setFormatter(main_formatter)

discord_handler = DiscordBotHandler()
discord_handler.setLevel(logging.DEBUG)
discord_handler.setFormatter(main_formatter)

root_logger.addHandler(console)
root_logger.addHandler(file)
root_logger.addHandler(discord_handler)

discord_handler.addFilter(Filter())

logging.config.fileConfig('log_config.ini')

client.run(TOKEN)
