import discord
from database import get_data,insert_data
from setting import signup_id,new_mention_id,embed_color
from discord.ext import commands
from datetime import datetime



class Register(commands.Cog, name='registrar'):
  '''These are the registration commands'''

  def __init__(self, bot):
	  self.bot = bot


  @commands.command(
    name = "register",
    brief = "Anyone can use this command to register with frat database",
  )
  async def Register(self,ctx):
    if not await get_data("SELECT * FROM `frat_users` WHERE discordid = %s",(ctx.author.id,)):
      await ctx.send(embed=discord.Embed(title=f"{ctx.author.name} Check Your DM's", color=embed_color, timestamp=datetime.utcnow()))
      def check(m):
          return m.author == ctx.author and m.channel == ctx.author.dm_channel
      await ctx.author.send(embed=discord.Embed(title="What is your first name?", color=embed_color, timestamp=datetime.utcnow()))
      first_name = (await self.bot.wait_for('message', check=check)).content
      await ctx.author.send(embed=discord.Embed(title="What is your last name?", color=embed_color, timestamp=datetime.utcnow()))
      last_name = (await self.bot.wait_for('message', check=check)).content
      await ctx.author.send(embed=discord.Embed(title="What is your email?",description="If you don't want to supply an email type N/A", color=embed_color, timestamp=datetime.utcnow()))
      email = (await self.bot.wait_for('message', check=check)).content
      await ctx.author.send(embed=discord.Embed(title="What is your phone number?",description="If you don't want to supply a phone number type N/A", color=embed_color, timestamp=datetime.utcnow()))
      phone_number = (await self.bot.wait_for('message', check=check)).content
      await ctx.author.send(embed=discord.Embed(title="What is your graduation year?", color=embed_color, timestamp=datetime.utcnow()))
      grade = (await self.bot.wait_for('message', check=check)).content
      name=ctx.author.name
      await insert_data("INSERT INTO `frat_users`(`discordid`, `Discord_Name`, `First_Name`, `Last_Name`, `Email`, `Phone_Number`, `Graduation_Year`) VALUES (%s,%s,%s,%s,%s,%s,%s)",(ctx.author.id,name,first_name,last_name,email,phone_number,grade))
      embed = discord.Embed(title="Your Info",color=embed_color)
      embed.add_field(name="Name",value=f"{first_name} {last_name}",inline=False)
      embed.add_field(name="Email",value=email)
      embed.add_field(name="Phone Number",value=phone_number)
      embed.add_field(name="Graduation Year",value=grade)
      await ctx.author.send(embed=embed)
      embed=discord.Embed(title=f"New User has singed up, here's the info for {ctx.author.mention}",color=embed_color)
      embed.add_field(name="Email",value=email)
      embed.add_field(name="Phone Number",value=phone_number)
      embed.add_field(name="Graduation Year",value=grade)

      guild = ctx.guild
      channel = guild.get_channel(signup_id)
      admins = guild.get_role(new_mention_id)
      await ctx.send(f"Hey {admins.mention} {ctx.author.mention} just signed up!")
      await channel.send(embed=embed)
    else:

      await ctx.send(embed=discord.Embed(title="You've already signed up, please use !updateprofile if you need to change any settings",color=embed_color))

  @commands.command(
    name = "updateprofile",
    brief = "Use this command to update your profile info.",
  )
  async def updateprofile(self,ctx):
    await ctx.send(embed=discord.Embed(title="Check your DM's for instructions!"))
    message = await ctx.author.send(embed=discord.Embed(title="React with the matching emoji for what you want to change",description="1️⃣: First Name\n\n2️⃣: Last name\n\n3️⃣: Email\n\n4️⃣: Phone number\n\n5️⃣: Graduation year",color=embed_color))
    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")
    await message.add_reaction("3️⃣")
    await message.add_reaction("4️⃣")
    await message.add_reaction("5️⃣")

    def reactcheck(reaction, user):
            return user == ctx.author 
    
    def check(m):
          return m.author == ctx.author and m.channel == ctx.author.dm_channel
        

    reaction, user = await self.bot.wait_for('reaction_add',check=reactcheck)
    if reaction.emoji == "1️⃣":
      await ctx.author.send(embed=discord.Embed(title="What is your updated first name?", color=embed_color, timestamp=datetime.utcnow()))
      new_data = (await self.bot.wait_for('message', check=check)).content

      await insert_data("UPDATE `frat_users` SET `First_Name`=%s WHERE `discordid` = %s",(new_data,ctx.author.id))

      await ctx.author.send(embed=discord.Embed(title=f"First name updated to {new_data}",description='Run !updateprofile again to change other data',color=embed_color))
    elif reaction.emoji == "2️⃣":
      await ctx.author.send(embed=discord.Embed(title="What is your updated last name?", color=embed_color, timestamp=datetime.utcnow()))
      new_data = (await self.bot.wait_for('message', check=check)).content

      await insert_data("UPDATE `frat_users` SET `Last_Name`=%s WHERE `discordid` = %s",(new_data,ctx.author.id))

      await ctx.author.send(embed=discord.Embed(title=f"Last name updated to {new_data}",description='Run !updateprofile again to change other data',color=embed_color))
    elif reaction.emoji == "3️⃣":
      await ctx.author.send(embed=discord.Embed(title="What is your updated email?", color=0xFF0000, timestamp=datetime.utcnow()))
      new_data = (await self.bot.wait_for('message', check=check)).content

      await insert_data("UPDATE `frat_users` SET `Email`=%s WHERE `discordid` = %s",(new_data,ctx.author.id))

      await ctx.author.send(embed=discord.Embed(title=f"Email updated to {new_data}",description='Run !updateprofile again to change other data',color=embed_color))
    elif reaction.emoji == "4️⃣":
      await ctx.author.send(embed=discord.Embed(title="What is your updated phone number?", color=embed_color, timestamp=datetime.utcnow()))
      new_data = (await self.bot.wait_for('message', check=check)).content

      await insert_data("UPDATE `frat_users` SET `Phone_Number`=%s WHERE `discordid` = %s",(new_data,ctx.author.id))

      await ctx.author.send(embed=discord.Embed(title=f"Phone number updated to {new_data}",description='Run !updateprofile again to change other data',color=embed_color))
    elif reaction.emoji == "5️⃣":
      await ctx.author.send(embed=discord.Embed(title="What is your updated graduation year?", color=embed_color, timestamp=datetime.utcnow()))
      new_data = (await self.bot.wait_for('message', check=check)).content

      await insert_data("UPDATE `frat_users` SET `Graduation_Year`=%s WHERE `discordid` = %s",(new_data,ctx.author.id))

      await ctx.author.send(embed=discord.Embed(title=f"Graduation year updated to {new_data}",description='Run !updateprofile again to change other data',color=embed_color))
    
  @commands.command(
    name = "profile",
    brief = "Gets a user profile, can mention a user to get their stats",
  )
  async def profile(self,ctx,args=""):
    if not args:        
      embed=discord.Embed(title=f"Contact info for {ctx.author.name}",color=embed_color)
      embed.set_thumbnail(url = ctx.author.avatar_url)
      user_id=ctx.author.id
    else:
      args = args[3:]
      args=args.replace(">","")
      user = self.bot.get_user(int(args))
      embed=discord.Embed(title=f"Contact info for {user.name}",color=embed_color)
      embed.set_thumbnail(url = user.avatar_url)
      user_id=user.id
    data = (await get_data("SELECT `First_Name`, `Last_Name`, `Email`, `Phone_Number`, `Graduation_Year` FROM `frat_users` WHERE discordid=%s",(user_id,)))[0]
    embed.add_field(name='Name',value=f"{data[0]} {data[1]}",inline=False)
    embed.add_field(name='Email',value=data[2])
    embed.add_field(name='Phone number',value=data[3])
    embed.add_field(name='Graduation year',value=data[4])
    await ctx.send(embed=embed)


        
      


def setup(bot):
	bot.add_cog(Register(bot))

