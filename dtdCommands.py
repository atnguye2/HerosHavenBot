import discord
from discord.ext import commands
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from InitializeHerosHavenDataBase import Base, User


print('Connecting to database')
engine = create_engine('sqlite:///HeroHavenDatabase.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
# new_user = User(userid='142441829185355776', dtd=10)
# session.add(new_user)
# session.commit()


class dtdCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description='This is a command that modifies downtime days', pass_context=True)
    async def dtd(self, ctx, change: int = 0):
        try:
            user = session.query(User).filter(User.userid == str(ctx.message.author.id)).one()
            print("User found. Doing stuff")
            user.dtd += change
            session.commit()
            await ctx.send("{User} now has {dtd} downtime days!".format(dtd=str(user.dtd), User=str(ctx.message.author.name)))
        except sqlalchemy.orm.exc.NoResultFound:
            print("Adding User to DB")
            new_user = User(userid=str(ctx.message.author.id), dtd=change)
            session.add(new_user)
            session.commit()
            await ctx.send("{User} now has {change} downtime days!".format(change=str(change), User=str(ctx.message.author.name)))

    @commands.command(description = 'This is a command to track creatures left with one hp.', pass_context=True)
    async def ohp(self, ctx, change: int = 0):
        try:
            user = session.query(User).filter(User.userid == str(ctx.message.author.id)).one()
            print("User found. Doing stuff")
            user.ohp += change
            await ctx.send("{User} now has {ohp} one hit point creatures!".format(ohp=str(user.ohp), User=str(ctx.message.author.name)))
        except:
            print("Adding User to DB")
            new_user = User(userid=str(ctx.message.author.id), ohp=change)
            session.add(new_user)
            session.commit()
            await ctx.send("{User} now has {change} one hit point creatures!".format(change=str(change), User=str(ctx.message.author.name)))

def setup(client):
    client.add_cog(dtdCommands(client))
