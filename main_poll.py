from discord.ext import commands
import discord
import yaml

import bollsvenskan as bs

intents = discord.Intents.default()

CLIENT = commands.Bot(command_prefix="!", intents=intents)

MESSAGE_ID = None
CHANNEL_ID = None
TOKEN = None

def initConfig():
    global TOKEN, CHANNEL_ID, MESSAGE_ID

    with open('/bin/config.yaml') as f:
        y = yaml.load(f, Loader=yaml.FullLoader)
        TOKEN = y["TOKEN"]
        CHANNEL_ID = y["CHANNEL_ID"]
        MESSAGE_ID = y["MESSAGE_ID"]

@CLIENT.event
async def on_ready():   
    message = await CLIENT.get_channel(CHANNEL_ID).fetch_message(MESSAGE_ID)
    await message.clear_reactions()

    message = await CLIENT.get_channel(CHANNEL_ID).fetch_message(MESSAGE_ID)
    await message.edit(content="```ansi\n" + bs.BollSvenskan().getList() + "```")

if __name__ == "__main__":
    print("running main_poll.py")
    
    initConfig()
    CLIENT.run(TOKEN)