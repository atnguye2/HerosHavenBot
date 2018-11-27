AFFIRMATIVE_REPLIES = ["Y", "T", "M", "y", "t", "m"]

def round_nearest_half(number):
    return round(number * 2) / 2

def getHelpCommand():
    messageContent = """
```md
react: A tool used to add a number of regional indicator symbols to a post. Useful for voting. Enable the Discord option under Settings -> Appearance -> Advanced -> Developer Mode to get channel and message IDs.
    
    Usage:+react channelID messageID numberOfOptions
    
    channelID: The ID of the text channel of the target message.
    messageID: The ID of the target message.
    numberOfOptions: An integer 1-20. This is the number of regional indicator emojis that will be replied.

dmxp: Calculates DM Rewards for a given DMPC based on their level and the hours DMd in a session.

	Usage: +dmxp dmpcLevel hoursPlayed [isMultishot]

	dmpcLevel: The level of the DM Character
	hoursPlayed: The number of hours played. Can be a decimal, such as 3.25.
	isMultishot: Optional. Whether these rewards were for a multishot. Acceptable values are (M)ultishot, (T)rue/(Y)es or (F)alse/(N)o. Default is no.	
```
"""
    return messageContent