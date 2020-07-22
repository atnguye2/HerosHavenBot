import sqlalchemy
from discord.ext import commands
import discord
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from InitializeHerosHavenDataBase import Base, Character, User
import commandHelpers

engine = create_engine('sqlite:///HeroHavenDatabase.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

class characterCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(description='This is a command to help track your characters. +char will list your characters. +char new will prompt you to add a new character. +char edit will prompt you to edit existing characters.', pass_context=True)
    async def char(self, ctx):
        try:
            session = DBSession()
            characters = session.query(Character).filter(Character.userid == str(ctx.message.author.id)).all()
            if not characters:
                await self.client.say("No characters found for {User}. Please use **+char new** to add one.".format(User=str(ctx.message.author.name)))
            session.commit()
            charOutput = ""
            i = 1
            for character in characters:
                charOutput += "**"+ str(i) + "**: " + character.charName + " with " + str(character.charExp) + " experience points, " + str(character.charGold) + " gold pieces, and " + str(character.charResiduum) + " raw residuum. \n"
                i += 1
            charOutput += "\n\nPlease use **+char new** to add a new character. \n"
            charOutput += "To edit an existing character, use **+char edit**"
            embed = discord.Embed(
                title = ctx.message.author.name + "'s current characters:",
                description = charOutput,
                colour = commandHelpers.getRandomHexColor()
            )
            await ctx.send(ctx.message.channel, embed=embed)
        except sqlalchemy.orm.exc.NoResultFound:
            print("Adding {User} to User table")
            new_user = User(userid=str(ctx.message.author.id), dtd = 0)
            session.add(new_user)
            session.commit()
            await ctx.send("{User} now has been added to the User table!".format(User=str(ctx.message.author.name)))
    @char.command(pass_context=True)
    async def new(self, ctx):
        await ctx.send("{User} wants to add a new character.".format(User=str(ctx.message.author.name)))
        await ctx.send("What is this character's name?")
        cName = await self.client.wait_for_message(author=ctx.message.author, timeout=180)
        cName = str(cName.content)
        await ctx.send("How much experience does " + cName + " currently have?")
        cXp = await self.client.wait_for_message(author=ctx.message.author, timeout=180)
        await ctx.send("How much gold does " + cName + " currently have?")
        cGold = await self.client.wait_for_message(author=ctx.message.author, timeout=180)
        await ctx.send("How much raw residuum does " + cName + " currently have?")
        cResi = await self.client.wait_for_message(author=ctx.message.author, timeout=180)
        try:
            cXp = int(cXp.content)
            cGold = int(cGold.content)
            cResi = int(cResi.content)
        except:
            await ctx.send("That didn't work. Make sure you use an integer.")
        new_character = Character(userid = str(ctx.message.author.id), charName = cName, charExp = cXp, charGold = cGold, charResiduum = cResi)
        session = DBSession()
        try:
            session.add(new_character)
            session.commit()
            await ctx.send(cName + " has been added to your roster!")
        except:
            await ctx.send("Character was not saved!")
            session.rollback()

    @char.command(pass_context=True)
    async def edit(self, ctx):
        session = DBSession()
        characters = session.query(Character).filter(Character.userid == str(ctx.message.author.id)).all()
        await ctx.send("Select the character to edit by entering the number.")
        charNum = await self.client.wait_for_message(author=ctx.message.author, timeout=180)
        charNum = int(charNum.content) - 1
        selectedChar = characters[charNum]
        await ctx.send("You selected " + str(charNum + 1) + " " + selectedChar.charName)
        await ctx.send("Enter the new amounts for XP, GP, and Res. All three are required. Separate each integer with a space.")
        newValues = await self.client.wait_for_message(author=ctx.message.author, timeout=180)
        try:
            aryNewValues = newValues.content.split()
            newXP = int(aryNewValues[0])
            newGP = int(aryNewValues[1])
            newRes = int(aryNewValues[2])
        except:
            await ctx.send("Probably bad input. Use integers with spaces in between. Example: 900 50 0")
        try:
            selectedChar.charExp = newXP
            selectedChar.charGold = newGP
            selectedChar.charResiduum = newRes
            session.commit()
            await ctx.send(selectedChar.charName + " has been updated.")
        except:
            await ctx.send(selectedChar.charName + " did not save!.")
            session.rollback()


def setup(client):
    client.add_cog(characterCommands(client))