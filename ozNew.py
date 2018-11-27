import discord
from discord.ext import commands


# This is the token found under the https://discordapp.com/developers/applications/509871894061907970/bots
# It it currently tied to Brad's Discord account

# Debug
DISCORD_BOT_TOKEN = 'NDkyMDE3NDY1MDI3NTkyMjAz.Dt4YGw.exS2x9R7A7e2ory4IGPOiC8aUDE'

# Live
# DISCORD_BOT_TOKEN = 'NTA5ODcxODk0MDYxOTA3OTcw.DsUSEA.KWPIudgcPe7ciBHiMaUZcZrdMm4'


# Requires Discord Webhooks to do anything too terribly interesting.
gamePresence = discord.Game(name="+help")

client = commands.Bot(command_prefix='+', pass_context=True, description='')
startup_extensions = ['ungroupedCommands','dtdCommands']


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print(discord.__version__)
    await client.change_presence(game=gamePresence, afk=False, status=None)


@client.event
async def on_message(msg):
    await client.process_commands(msg)


@client.command()
async def load(extension_name: str):
    """Loads an extension."""
    try:
        client.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await client.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await client.say("{} loaded.".format(extension_name))


for extension in startup_extensions:
    try:
        print('Loading '+str(extension))
        client.load_extension(extension)
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Failed to load extension {}\n{}'.format(extension, exc))


# Warning This function must be the last function to call due to the fact that it is blocking.
# That means that registration of events or anything being called after
# this function call will not execute until it returns.
client.run(DISCORD_BOT_TOKEN)
