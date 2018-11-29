from discord.ext import commands
import reactMenu as rM
import discord
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from InitializeHerosHavenDataBase import Base, Vote


# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
engine = create_engine('sqlite:///HeroHavenDatabase.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class voteCommands():
    def __init__(self, client):
        self.client = client

    @commands.group(pass_context=True, description='A set of commands to help with making and voting on polls')
    async def vote(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.client.say('Type +help vote for more help')

    @vote.command(pass_context=True)
    @commands.has_any_role('mods', 'loremasters', 'logisticians', 'techromancer')
    async def c(self, ctx):
        pollTypes = ["Staff", "Logic", "Lore", "Public"]
        #pollChan = ['514670013706403850','509566067757285406','509566093799718932','509454369192673291']
        pollChan = ['427846372168040452', '427846372168040452', '427846372168040452', '427846372168040452']
        embed = discord.Embed(
            title='What type of poll do you want',
            descption='What channel does this poll belong to',
            colour=discord.Color.dark_purple()
        )
        embed.add_field(name="1 "+pollTypes[0], value="Open to all staff to vote on", inline=False)
        embed.add_field(name="2 "+pollTypes[1], value="Open to logic team to vote on", inline=False)
        embed.add_field(name="3 "+pollTypes[2], value="Open to lore team to vote on", inline=False)
        embed.add_field(name="4 "+pollTypes[3], value="Open to the public to vote on", inline=False)
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
        await self.client.send_message(targetChannel, embed=embed)
        async for msgs in self.client.logs_from(targetChannel, limit=1):
            botMessage = msgs
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
        for x in range(1, len(options.content)+1):
            y = emoji[x]
            await self.client.add_reaction(botMessage, emoji=y)

            newVote = Vote(
                            voteTitle=question.content,
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
        allVotes = session.query(Vote).filter(Vote.voteDone == 0).all()
        embed = discord.Embed(
            title='Which poll do you want to tally?',
            descption='Shown below are the questions',
            colour=discord.Color.dark_purple()
        )
        for c, v in enumerate(allVotes):
            embed.add_field(name=str(c+1), value=v.voteTitle, inline=False)
            print(c,v.voteTitle)
        choice = await rM.Menu(self.client).menu(ctx, 1, embed, allVotes)
        print(choice)
        choice = allVotes[choice-1]
        choice.voteDone = 1
        pollTypes = ["Staff", "Logic", "Lore", "Public"]
        pollChan = ['427846372168040452', '427846372168040452', '427846372168040452', '427846372168040452']
        channel = self.client.get_channel(pollChan[pollTypes.index(choice.voteCategory)])
        message = await self.client.get_message(channel, choice.messageID)
        counts = {react.emoji: react.count for react in message.reactions}
        print(counts)
        winner = max(counts, key=counts.get)
        choice.voteDecision = winner
        session.commit()
        await self.client.say("The winner is {win} {option}".format(win=str(winner),
                                                                    option=choice.voteOptions.split('\n')[counts[winner]-1]))


def setup(client):
    client.add_cog(voteCommands(client))
