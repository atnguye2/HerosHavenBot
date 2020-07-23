import discord
import asyncio
from discord.ext import commands
from googleSheets import getWelcomeText

#PRODUCTION SERVER
CHANNELID = '604908914349309953'
ROLEMESSAGEID = '604934014402297857'

# general (test server) channel id
# #382727824001335297
#TESTSERVER
#CHANNELID = '382727824001335297'
#ROLEMESSAGEID = '600872091075477521'

#mid = '600884478126063637'

# This is the token found under the https://discordapp.com/developers/applications/509871894061907970/bots
# It it currently tied to Brad's Discord account
# Change this for production or debug...
#TESTINGTOKEN.txt is tied to "oz testing" a bot tied to Brad's discord acct.
#DEBUGTOKEN.txt is currently tied to Oz on the HH server
with open('TESTINGTOKEN.txt', 'r') as myfile:
    DISCORD_BOT_TOKEN = myfile.read()



# Requires Discord Webhooks to do anything too terribly interesting.
gamePresence = discord.Game(name="+help")

client = commands.Bot(command_prefix='+', pass_context=True, description='')
startup_extensions = ['ungroupedCommands','dtdCommands','voteCommands', 'characterCommands']

#the client won't listen for reactions on messages not in the client.messages queue. The current max size of this is 5000. To mitigate the chance that reaction message is not in the queue, we will add it every 10 minutes.
async def append_reaction_message(myChannelID, myMessageID):
    print("starting append_reaction_message()")
    myChannel = client.get_channel(myChannelID)
    myMessage = await client.get_message(myChannel, myMessageID)
    while True:
        print(str(len(client.messages)) + " Messages held in client.messages. Adding the Role Reaction Post now.")
        client.messages.append(myMessage)
        await asyncio.sleep(3600)
    print("ending append_reaction_message")

#async def fill_queue(myChannelID, myMessageID):
#    myChannel = client.get_channel(myChannelID)
#    myMessage = await client.get_message(myChannel, myMessageID)
#    for x in range(5005):
#        print(str(len(client.messages)) + " Messages held in client.messages. WOMP.")
#        client.messages.append(myMessage)


@client.event
async def on_ready():
    #await fill_queue(CHANNELID, mid)
    print('We have logged in as {0.user}'.format(client))
    print('We are using discord.py version ' +  discord.__version__)
    await client.change_presence(activity=gamePresence, afk=False, status=None)
    await append_reaction_message(CHANNELID, ROLEMESSAGEID)

@client.event
async def on_message(msg):
    await client.process_commands(msg)



@client.event
async def on_member_join(ctx):
    print(ctx.name + ' has joined. Lets make them a player!'.format(client))
    print(getWelcomeText())
    await client.send_message(ctx, getWelcomeText())




#Beware that the player role needs to be of lower hierchy than the role assigned to the bot.
@client.event
async def on_reaction_add(reaction, user):
    print("a reaction add!")
    print(reaction.message.id)
    print(client.messages)
    if reaction.message.id == ROLEMESSAGEID:
        print(reaction.emoji)
        if reaction.emoji == "🎲":
            print("OK player here 1")
            role = discord.utils.get(user.server.roles, name="players")
            await client.add_roles(user, role)
        if reaction.emoji == "🏰":
            print("OK DM here")
            role = discord.utils.get(user.server.roles, name="DMs")
            await client.add_roles(user, role)
        if reaction.emoji == "🐲":
            print("OK PF here")
            role = discord.utils.get(user.server.roles, name="Pathfinder")
            await client.add_roles(user, role)
        else:
            return
    else:
        return

@client.event
async def on_reaction_remove(reaction, user):
    print("a reaction remove!")
    if reaction.message.id == ROLEMESSAGEID:
        print(reaction.emoji)
        if reaction.emoji == "🎲":
            print("attempt to remove player role")
            role = discord.utils.get(user.server.roles, name="players")
            await client.remove_roles(user, role)
        if reaction.emoji == "🏰":
            print("attempt to remove DM role")
            role = discord.utils.get(user.server.roles, name="DMs")
            await client.remove_roles(user, role)
        if reaction.emoji == "🐲":
            print("attempt to remove PF role")
            role = discord.utils.get(user.server.roles, name="Pathfinder")
            await client.remove_roles(user, role)
        else:
            return
    else:
        return

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