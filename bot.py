from discord.ext import commands
import discord
import yaml

import bollsvenskan as bs

intents = discord.Intents.default()
intents.members = True

CLIENT = commands.Bot(command_prefix="!", intents=intents)
EMOJIS = ['✅', '✔️', '☑️']

MESSAGE_ID = None
CHANNEL_ID = None
TOKEN = None

def initConfig():
    global TOKEN, CHANNEL_ID

    with open('config.yaml') as f:
        y = yaml.load(f, Loader=yaml.FullLoader)
        TOKEN = y["TOKEN"]
        CHANNEL_ID = y["CHANNEL_ID"]

        print(CHANNEL_ID)

@CLIENT.event
async def on_ready():
    global MESSAGE_ID
    
    print(f"{CLIENT.user} Bois, I'm in")
    
    channel = CLIENT.get_channel(CHANNEL_ID)
    message = await channel.send("```ansi\n" + bs.BollSvenskan().getList() + "```")
    MESSAGE_ID = message.id

    [await message.add_reaction(emoji) for emoji in EMOJIS]

async def reactionHelper(reaction, user, bool):
    if reaction.message.id == MESSAGE_ID and user.id != CLIENT.application.id:
        [print(user.name, i) if str(reaction.emoji) == EMOJIS[i] else None for i in range(len(EMOJIS))]
        [bs.BollSvenskan(user.name).sign(i, bool) if str(reaction.emoji) == EMOJIS[i] else None for i in range(len(EMOJIS))]

        message = await CLIENT.get_channel(CHANNEL_ID).fetch_message(MESSAGE_ID)
        await message.edit(content="```ansi\n" + bs.BollSvenskan().getList() + "```")

@CLIENT.event
async def on_reaction_add(reaction, user):
    await reactionHelper(reaction, user, True)

@CLIENT.event
async def on_reaction_remove(reaction, user):
    print(reaction)
    await reactionHelper(reaction, user, False)

@CLIENT.command()
async def TOKEN(ctx):
    author = ctx.message.author

    print(bs.BollSvenskan.tokenPairs, author.name)
    
    await author.send(bs.BollSvenskan.tokenPairs[author.name] if author.name in bs.BollSvenskan.tokenPairs else "You haven't signed up using me.")