from discord.ext import commands
import reactMenu as rM
import discord
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from InitializeHerosHavenDataBase import Base, Vote


# Bind the engine to the metadata of the Base class so that the
# declarative can be accessed through a DBSession instance
engine = create_engine('sqlite:///HeroHavenDatabase.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class voteCommands():
    def __init__(self, client):
        self.client = client

    # Create a commands group
    @commands.group(pass_context=True, description='A set of commands to help with making and voting on polls')
    async def vote(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.client.say('Type +help vote for more help')

    @vote.command(pass_context=True)
    @commands.has_any_role('mods', 'loremasters', 'logisticians', 'techromancer')
    async def c(self, ctx):
        pollTypes = ["Staff", "Logic", "Lore", "Public"]
        pollChan = ['514670013706403850','509566067757285406','509566093799718932','509454369192673291']
        #pollChan = ['427846372168040452', '427846372168040452', '427846372168040452', '427846372168040452']
        embed = discord.Embed(
            title='What type of poll do you want',
            descption='What channel does this poll belong to',
            colour=discord.Color.dark_purple()
        )
        embed.add_field(name="1 "+pollTypes[0], value="Open to all staff to vote on", inline=False)
        embed.add_field(name="2 "+pollTypes[1], value="Open to logic team to vote on", inline=False)
        embed.add_field(name="3 "+pollTypes[2], value="Open to lore team to vote on", inline=False)
        embed.add_field(name="4 "+pollTypes[3], value="Open to the public to vote on", inline=False)
        # Takes input from user via menu. Menu object constructed from module downloaded off git
        askPollType = await rM.Menu(self.client).menu(ctx,
                                                      1,
                                                      embed,
                                                      pollTypes)
        targetChannel = self.client.get_channel(pollChan[askPollType-1])
        await self.client.say("What is the question?")
        question = await self.client.wait_for_message(author=ctx.message.author, timeout=120)
        await self.client.say("Elaborate on the details.")
        details = await self.client.wait_for_message(author=ctx.message.author, timeout=180)
        await self.client.say("What are the options? Please write each option on a new line.")
        options = await self.client.wait_for_message(author=ctx.message.author, timeout=180)
        options.content = options.content.split('\n');
        embed = discord.Embed(
            title=question.content,
            descption=details.content,
            colour=discord.Color.dark_purple()
        )
        for c, v in enumerate(options.content):
            embed.add_field(name=str(c+1),
                            value=v,
                            inline=False)
        botMessage = await self.client.send_message(targetChannel, embed=embed)
        emoji = {
            0: "0⃣",
            1: "1⃣",
            2: "2⃣",
            3: "3⃣",
            4: "4⃣",
            5: "5⃣",
            6: "6⃣",
            7: "7⃣",
            8: "8⃣",
            9: "9⃣",
            10: "🔟"
        }
        # Add a reaction for every option present in the poll
        for x in range(1, len(options.content)+1):
            y = emoji[x]
            await self.client.add_reaction(botMessage, emoji=y)
        # Build a new Vote object to add to the database
        newVote = Vote( voteTitle=question.content,
                        voteCategory=pollTypes[askPollType-1],
                        voteDescription=details.content,
                        voteOptions="\n".join([v for v in options.content]),
                        messageID=botMessage.id
            )
        session.add(newVote)
        session.commit()

    @vote.command(pass_context=True)
    @commands.has_any_role('mods', 'loremasters', 'logisticians', 'techromancer')
    async def e(self, ctx):
        # Find all votes that have not finished. List of Vote objects.
        allVotes = session.query(Vote).filter(Vote.voteDone == 0).all()

        # Build an embed for the reaction menu.
        embed = discord.Embed(
            title='Which poll do you want to tally?',
            descption='Shown below are the questions',
            colour=discord.Color.dark_purple()
        )
        for c, v in enumerate(allVotes):
            embed.add_field(name=str(c+1), value=v.voteTitle, inline=False)
        # Use the reaction menu to have user select the poll.
        choice = await rM.Menu(self.client).menu(ctx, 1, embed, allVotes)
        # Output is an int. Subtract 1 for proper indexing
        choice = allVotes[choice-1]
        # Change the flag var in the database
        choice.voteDone = 1
        # Find the actual vote message to create the discord message object
        pollTypes = ["Staff", "Logic", "Lore", "Public"]
        pollChan = ['427846372168040452', '427846372168040452', '427846372168040452', '427846372168040452']
        channel = self.client.get_channel(pollChan[pollTypes.index(choice.voteCategory)])
        voteMessage = await self.client.get_message(channel, choice.messageID)
        # Count votes
        counts = {react.emoji: react.count for react in voteMessage.reactions}
        winner = max(counts, key=counts.get)
        # Change more attributes in database
        choice.voteDecision = winner
        session.commit()
        # Announce winner in the channel command was called in. Edit the vote message and clear reactions
        announcestr = "The winner is {win} {option}".format(win=str(winner),
                                                            option=choice.voteOptions.split('\n')[counts[winner]-1])
        await self.client.say(announcestr)
        await self.client.edit_message(voteMessage, voteMessage.content + '\nThe vote has ended \n' + announcestr)
        await self.client.clear_reactions(voteMessage)


def setup(client):
    client.add_cog(voteCommands(client))
