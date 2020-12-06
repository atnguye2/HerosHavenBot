import discord
import commandHelpers
import string
import unicodedata
import random
from discord.ext import commands
import googleSheets

# Read the Oz Config Google Sheets
dmxpRows = googleSheets.getDmXpRows()
flavorTextRows = googleSheets.getFlavorTextRows()
judgeTextRows = googleSheets.getJudgeTextRows()
resRows = googleSheets.getResRows()
pfxpRows = googleSheets.getPfXpRows()



class UngroupedCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description='This is a command that echos the input')
    async def echo(self, ctx, *sentence):
        # Repeat what the user inputs. This is an example
        msg = ''
        for word in sentence:
            msg += word
            msg += ' '
        await ctx.send(msg)

    @commands.command(description='This is a command that calculates DM rewards')
    async def dmxp(self, ctx, dmpcLevel, hoursPlayed, isMultishot='n'):
        hoursPlayed = commandHelpers.round_nearest_half(float(hoursPlayed))
        if any(n in isMultishot for n in commandHelpers.AFFIRMATIVE_REPLIES):
            multishotCoefficient = 1.2
            gameType = 'Multi-shot'
        else:
            multishotCoefficient = 1
            gameType = 'One-shot'

        print("multishotCoefficient = " + str(multishotCoefficient))
        selectedRow = (dmxpRows[int(dmpcLevel)])
        calculatedXP = int(selectedRow['xpHr']) * hoursPlayed
        calculatedGP = int(selectedRow['gpHr']) * hoursPlayed * multishotCoefficient
        calculatedRes = int(selectedRow['resHr']) * hoursPlayed * multishotCoefficient
        calculatedPCdtd = 2 * hoursPlayed
        calculatedDMdtd = 4 * hoursPlayed
        flavor = flavorTextRows[random.randint(0, 6)]['flavortext'] #random index based on the number of options defined in the google Sheets config
        msgOut = """
    {flavor}
    ```md
    DMPC {gameType} rewards for a level {dmpcLevel} character, adjusted to {hoursPlayed} hours played.
    DTD: Players: {calculatedPCdtd}, DM: {calculatedDMdtd}
    DMXP: {calculatedXP}
    DM Gold: {calculatedGP}
    DM Res: {calculatedRes}```"""
        msgOut = msgOut.format(flavor=str(flavor), gameType=str(gameType), dmpcLevel=str(dmpcLevel),
                               hoursPlayed=str(hoursPlayed), calculatedPCdtd=str(calculatedPCdtd),
                               calculatedDMdtd=str(calculatedDMdtd), calculatedXP=str(calculatedXP),
                               calculatedGP=str(calculatedGP), calculatedRes=str(calculatedRes))
        await ctx.send(msgOut)

        
    @commands.command(description='This is a command that adds reactions to a message', pass_context=True)
    async def react(self, ctx, numberOfOptions):
        myChannel = ctx.message.channel
        print(myChannel)
        numberOfOptions = int(numberOfOptions)
        async for msgs in myChannel.history(limit=1, before=ctx.message):
            myMessage = msgs
        for x in range(0, numberOfOptions):
            y = string.ascii_lowercase[x]
            y = "REGIONAL INDICATOR SYMBOL LETTER " + y
            await myMessage.add_reaction(emoji=unicodedata.lookup(y))

    @commands.command(description='This is a command created for the Liars Mask/Halloween event.')
    async def judge(self, ctx):
        judgement = judgeTextRows[random.randint(0, 6)]['judgetext'] #random index based on the number of options defined in the google Sheets config
        msgOut = """{flavor}"""
        msgOut = msgOut.format(flavor=str(judgement))
        await ctx.send(msgOut)

    @commands.command(description='This is a command that calculates Residuum rewards for 5e games', pass_context=True)
    async def res(self, ctx, totalXP, minpc, numPlayers=1, isMultishot='n'):
        if any(n in isMultishot for n in commandHelpers.AFFIRMATIVE_REPLIES):
            multishotCoefficient = 1.2
            gameType = 'Multi-shot'
        else:
            multishotCoefficient = 1
            gameType = 'One-shot'
        numPlayers = int(numPlayers)
        print("multishotCoefficient = " + str(multishotCoefficient))
        selectedRow = (resRows[int(minpc)])
        print(selectedRow)
        XPDenom = float(selectedRow['XPdenominator'])
        calculatedRes = int(totalXP) / XPDenom * multishotCoefficient
        maxMIFound = int(selectedRow['maxMI'])
        splitGold = int(calculatedRes) / numPlayers
        splitXP = int(totalXP) / numPlayers

        sheetlink = '[Crafting Sheet](https://docs.google.com/spreadsheets/d/1kXkZqB6xPjzv8p4J_afmmr6qiZZD_w6xL9XYRuQlRjs/edit?usp=sharing)'

        flavor = flavorTextRows[random.randint(0, 6)][
            'flavortext']  # random index based on the number of options defined in the google Sheets config
        msgOut = """
       {flavor}
       ```md
{gameType} rewards for a session with total of {totalXP} experience points across {numPlayers} players:
The lowest player character was level {minpc}, resulting in a modifier of {XPdenominator}.
       
Total Residuum Budget: {calculatedRes} for the group.
Maximum Single Magic Item Cost: {maxMIFound}
Maximum Total Gold: {calculatedRes}
Maximum Gold Per Player: {splitGold}
Experience Per Player: {splitXP}
           
       ```
{sheetlink}
       """
        msgOut = msgOut.format(flavor=str(flavor), gameType=str(gameType), minpc=str(minpc),
                               calculatedRes=str(round(calculatedRes)), XPdenominator=str(XPDenom),
                               totalXP=str(totalXP), maxMIFound=str(maxMIFound), splitGold=str(round(splitGold)),
                               splitXP=str(round(splitXP)), numPlayers=str(numPlayers), sheetlink=str(sheetlink))
        embed = discord.Embed(
            title="Session Rewards",
            description=msgOut,
            colour=commandHelpers.getRandomHexColor()
        )

        #embed.set_footer(text=sheetlink)

        await ctx.send(ctx.message.channel, embed=embed)

    @commands.command(description='This is a command that calculates Pathfinder session rewards')
    async def pfxp(self, ctx, pcLevel, hoursPlayed, difficultyCoefficient=1.0):
        hoursPlayed = commandHelpers.round_nearest_half(float(hoursPlayed))
        print("difficultyCoefficient = " + str(difficultyCoefficient))
        selectedRow = (pfxpRows[int(pcLevel)])
        calculatedXP = int(selectedRow['xpHr']) * hoursPlayed * difficultyCoefficient
        calculatedXP = int(calculatedXP)
        calculatedGP = int(selectedRow['gpHr']) * hoursPlayed * difficultyCoefficient
        calculatedGP = int(calculatedGP)
        msgOut = """    
    ```md
    Pathfinder one shot rewards for a level {pcLevel} character, adjusted to {hoursPlayed} hours played.
    Difficulty Modifier: {difficultyCoefficient}
    XP: {calculatedXP}
    Gold: {calculatedGP}```"""
        msgOut = msgOut.format(difficultyCoefficient=str(difficultyCoefficient), pcLevel=str(pcLevel),
                               hoursPlayed=str(hoursPlayed), calculatedXP=str(calculatedXP),
                               calculatedGP=str(calculatedGP))
        await ctx.send(msgOut)

def setup(client):
    client.add_cog(UngroupedCommands(client))
