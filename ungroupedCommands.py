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


class UngroupedCommands():
    def __init__(self, client):
        self.client = client

    @commands.command(description='This is a command that echos the input')
    async def echo(self, *sentence):
        # Repeat what the user inputs. This is an example
        msg = ''
        for word in sentence:
            msg += word
            msg += ' '
        await self.client.say(msg)

    @commands.command(description='This is a command that calculates DM rewards')
    async def dmxp(self, dmpcLevel, hoursPlayed, isMultishot='n'):
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
        await self.client.say(msgOut)

        
    @commands.command(description='This is a command that adds reactions to a message', pass_context=True)
    async def react(self, ctx, numberOfOptions):
        myChannel = ctx.message.channel
        print(myChannel)
        numberOfOptions = int(numberOfOptions)
        async for msgs in self.client.logs_from(myChannel, limit=1, before=ctx.message):
            myMessage = msgs
        for x in range(0, numberOfOptions):
            y = string.ascii_lowercase[x]
            y = "REGIONAL INDICATOR SYMBOL LETTER " + y
            await self.client.add_reaction(myMessage, emoji=unicodedata.lookup(y))



def setup(client):
    client.add_cog(UngroupedCommands(client))
