import discord
import asyncio
from discord.ext import commands
from setting import admin_roles, tickets_category,new_mention_id,embed_color


class Tickets(commands.Cog, name='support'):
  '''These are the developer commands'''

  def __init__(self, bot):
	  self.bot = bot


  @commands.command(  # Decorator to declare where a command is.
		name='ticket',  # Name of the command, defaults to function name.
    brief='Use this if you need a private channel to speak with frat heads'
	)
  async def ticket(self, ctx):
    """This command creates a ticket channel for a user"""
    guild = ctx.guild
    support = guild.get_role(new_mention_id)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True,send_messages=True),
        ctx.author: discord.PermissionOverwrite(read_messages=True,send_messages=True),
        support : discord.PermissionOverwrite(read_messages=True,send_messages=True),
    }
    category = guild.get_channel(tickets_category)
    channel = await guild.create_text_channel(f"{ctx.author.name} Ticket",overwrites=overwrites,category=category)
    await channel.send(f"{support.mention}, <@{ctx.author.id}>")
    await channel.send(embed=discord.Embed(title ='Ticket Channel',description=f"Please let us know your issue so we can help you\n<@{ctx.author.id}>, <@&{support.id}>",color=embed_color))
    await ctx.send(embed=discord.Embed(title = 'Ticket Created',description=f"Your ticket can be found in <#{channel.id}>",color=embed_color))

  @commands.command(
    name = "close",
    brief = "admins can use this to close a private channel",
  )
  @commands.has_any_role(*admin_roles)
  async def close(self,ctx):
    if ctx.channel.category.id==tickets_category:
      await ctx.send("Closing Ticket")
      await asyncio.sleep(5)
      await ctx.channel.delete()
    else:
      await ctx.send("This isn't a ticket channel")

	


def setup(bot):
	bot.add_cog(Tickets(bot))