from keep_alive import keep_alive
from discord.ext import commands
from setting import token


bot = commands.Bot(
	command_prefix="!",  # Change to desired prefix
	case_insensitive=True,  # Commands aren't case-sensitive

)

bot.author_id = 480055359462178826  # Change to your discord id!!!

@bot.event 
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier


extensions = [
	'cogs.cog_example','cogs.eblast','cogs.register','cogs.support','cogs.autoreact','cogs.last_fm','cogs.trivia','cogs.covid','cogs.help' # Same name as it would be if you were importing it
]

if __name__ == '__main__':  # Ensures this is the file being ran
	for extension in extensions:
		bot.load_extension(extension)  # Loades every extension.

keep_alive()  # Starts a webserver to be pinged.
bot.run(token)  # Starts the bot