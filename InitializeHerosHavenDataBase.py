from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import datetime
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'User'
    # Define columns for the table User
    userid = Column(String(250), primary_key=True)  # Discord ids tend to be long save as a string to avoid overflow
    dtd = Column(Integer)  # Downtime Days
    ohp = Column(Integer, nullable=False)  # one hp creatures
    user = relationship("Character", backref="parent")  # Establish a 1-Many relationship


class Character(Base):
    __tablename__ = 'Character'
    # Define columns for the table Character
    userid = Column(String(250), ForeignKey('User.userid'))  # Link a character to a user
    charid = Column(Integer, primary_key=True)  # Unique character id. Will autoincrement and doesn't need to be defined
    charName = Column(String(250), nullable=False)  # Character name
    charExp = Column(Integer, nullable=False)  # Character experience
    charGold = Column(Integer, nullable=False)  # Character gold
    charResiduum  = Column(Integer, nullable=False)  # Character residuum
#     charRace = Column(String(250))  # Character race
#     charSTR = Column(Integer)  # Character Strength Score
#     charCON = Column(Integer)  # Character Constitution Score
#     charDEX = Column(Integer)  # Character Dexterity Score
#     charINT = Column(Integer)  # Character Intelligence Score
#     charWIS = Column(Integer)  # Character Wisdom Score
#     charCHA = Column(Integer)  # Character Charisma Score
#     charSKILLS = Column(String(250))  # String that indicates proficiency. 0 = NonProf; 1 = Prof; 2 = Expertise

class Vote(Base):
    __tablename__ = 'voteDocket'
    voteid = Column(Integer, primary_key=True)
    voteTitle = Column(String(2500))
    voteCategory = Column(String(25))
    voteDescription = Column(String(2500))
    voteOptions = Column(String(2500))
    voteTime = Column(DateTime, default=datetime.datetime.utcnow(),onupdate=datetime.datetime.utcnow())
    voteDone = Column(Integer, default=0)
    voteDecision = Column(Integer, nullable=True)
    messageID = Column(String(30), nullable=True)





# Create an engine that stores data in the local directory's
# HeroHavenDatabase.db file.
engine = create_engine('sqlite:///HeroHavenDatabase.db', echo=True)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
