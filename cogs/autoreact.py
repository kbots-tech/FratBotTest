from setting import suggestion_channel
from discord.ext import commands


class Tickets(commands.Cog, name='autoreact'):
  '''These are the developer commands'''

  def __init__(self, bot):
	  self.bot = bot

  @commands.Cog.listener()
  async def on_message(self, message):
      if message.channel.id == suggestion_channel:
            await message.add_reaction("✅")
            await message.add_reaction("❌")

	


def setup(bot):
	bot.add_cog(Tickets(bot))