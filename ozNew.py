import discord
from discord.ext import commands
from googleSheets import getWelcomeText

#PRODUCTION SERVER
#New introductory rules post 784671120338976769
#5e rules post 784671578763821056
#pf rules post 784649797101158416
#Original ROLEMESSAGEID = 604934014402297857

roleMessagesList = [604934014402297857, 784671120338976769, 784671578763821056, 784649797101158416]

#TEST SERVER
#ROLEMESSAGEID = 785227588527587348

# This is the token found under the https://discordapp.com/developers/applications/509871894061907970/bots
# It it currently tied to Asuperbnames's Discord account
# Change this for production or debug...
#TESTINGTOKEN.txt is tied to "oz testing" a bot tied to Brad's discord acct.
#DEBUGTOKEN.txt is currently tied to Oz on the HH server
with open('DEBUGTOKEN.txt', 'r') as myfile:
    DISCORD_BOT_TOKEN = myfile.read()


# Requires Discord Webhooks to do anything too terribly interesting.
gamePresence = discord.Game(name="+help")

#Intents.members is required for on_member_join() event.
intnts = discord.Intents.default()
intnts.members = True

client = commands.Bot(command_prefix='+', pass_context=True, description='', intents=intnts)
startup_extensions = ['ungroupedCommands','dtdCommands','voteCommands', 'characterCommands']


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print('We are using discord.py version ' +  discord.__version__)
    await client.change_presence(activity=gamePresence, afk=False, status=None)


@client.event
async def on_message(msg):
    await client.process_commands(msg)


@client.event
async def on_member_join(ctx):
    print(getWelcomeText())
    await ctx.send(getWelcomeText())


#Beware that the roles added or deleted need to be of lower hierchy than the highest role assigned to the bot.
@client.event
async def on_raw_reaction_add(ctx):
    print("a raw reaction add!")
    if ctx.message_id in roleMessagesList:
        guild = client.get_guild(ctx.guild_id)
        roles = guild.roles
        member = ctx.member
        selected_role = 'nothing selected'
        print(member.name + " has reacted to the role post with " + ctx.emoji.name)
        if ctx.emoji.name == "🎲":
            selected_role = '5e'
        if ctx.emoji.name == "🛤️":
            selected_role = 'Pathfinder'
        if ctx.emoji.name == "📝":
            selected_role = 'play by post'
        if ctx.emoji.name ==  "🎭":
            selected_role = 'roleplay'
        if ctx.emoji.name == "🕴️":
            selected_role = 'pf roleplay'
        if ctx.emoji.name == "🗣️":
            selected_role = '5e roleplay'
        if ctx.emoji.name == "🦉":
            selected_role = 'Observer'
        if ctx.emoji.name == "🧙":
            selected_role = 'looking for game'

        print("A new " + selected_role + "!")
        for r in roles:
            if r.name == selected_role:
                role_to_change = r
                print("Found a role to add or delete!")
                print("trying to give " + member.name + " the role of " + role_to_change.name)
                await member.add_roles(r)
    else:
        #raw reaction change to a message we aren't listening on.
        return


@client.event
async def on_raw_reaction_remove(ctx):
    print("a raw reaction removal!")
    if ctx.message_id in roleMessagesList:
        guild = client.get_guild(ctx.guild_id)
        roles = guild.roles
        member = await guild.fetch_member(ctx.user_id)
        print(member.name + "has removed a reaction to the role post: " + ctx.emoji.name)
        if ctx.emoji.name == "🎲":
            selected_role = '5e'
        if ctx.emoji.name == "🛤️":
            selected_role = 'Pathfinder'
        if ctx.emoji.name == "📝":
            selected_role = 'play by post'
        if ctx.emoji.name ==  "🎭":
            selected_role = 'roleplay'
        if ctx.emoji.name == "🕴️":
            selected_role = 'pf roleplay'
        if ctx.emoji.name == "🗣️":
            selected_role = '5e roleplay'
        if ctx.emoji.name == "🦉":
            selected_role = 'Observer'
        if ctx.emoji.name == "🧙":
            selected_role = 'looking for game'

        print("A departing " + selected_role + "!")
        for r in roles:
            if r.name == selected_role:
                role_to_change = r
                print("Found a role to add or delete!")
                print("trying to relieve " + member.name + " of the role of " + role_to_change.name)
                await member.remove_roles(r)
    else:
        # raw reaction change to a message we aren't listening on.
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