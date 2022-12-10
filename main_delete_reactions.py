from discord.ext import commands
import discord
import yaml

intents = discord.Intents.default()

CLIENT = commands.Bot(command_prefix="!", intents=intents)
EMOJIS = ['✅', '✔️', '☑️']

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

    [await message.add_reaction(emoji) for emoji in EMOJIS]

if __name__ == "__main__":
    print("running main_delete_reactions.py")
    
    initConfig()
    CLIENT.run(TOKEN)