import discord
from discord.ext import commands


# This is the token found under the https://discordapp.com/developers/applications/509871894061907970/bots
# It it currently tied to Brad's Discord account

# Change this for production or debug...
#TESTINGTOKEN.txt is tied to "oz testing" a bot tied to Brad's discord acct.
#DEBUGTOKEN.txt is currently tied to Oz on the HH server
with open('DEBUGTOKEN.txt', 'r') as myfile:
    DISCORD_BOT_TOKEN = myfile.read()



# Requires Discord Webhooks to do anything too terribly interesting.
gamePresence = discord.Game(name="+help")

client = commands.Bot(command_prefix='+', pass_context=True, description='')
startup_extensions = ['ungroupedCommands','dtdCommands','voteCommands']


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print(discord.__version__)
    await client.change_presence(game=gamePresence, afk=False, status=None)


@client.event
async def on_message(msg):
    await client.process_commands(msg)

#When a new user joins the server, add the role 'player'
#Beware that the player role needs to be of lower hierchy than the role assigned to the bot.
@client.event
async def on_member_join(ctx):
    print(ctx.name + ' has joined. Lets make them a player!'.format(client))
    role = discord.utils.get(ctx.server.roles, name="players")
    await client.add_roles(ctx, role)

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
