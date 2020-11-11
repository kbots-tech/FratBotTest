import discord
import smtplib
from database import get_data
from setting import admin_roles,email,email_password,email_signature,embed_color
from discord.ext import commands
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



class EBlast(commands.Cog, name='eblast'):
  '''These are the registration commands'''

  def __init__(self, bot):
	  self.bot = bot

  @commands.command(
    name = "eblast",
    brief = "admins can use this to send an eblast to all members in the database",
  )
  @commands.has_any_role(*admin_roles)
  async def eblast(self,ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.author.dm_channel
    await ctx.author.send(embed=discord.Embed(title="What is the subject?", color=embed_color))
    message_subject = (await self.bot.wait_for('message', check=check)).content  
    await ctx.author.send(embed=discord.Embed(title="What is the message body?", color=embed_color))
    message_body = f"{(await self.bot.wait_for('message', check=check)).content} \n\n\n {email_signature}"
    emails = [f[0] for f in (await get_data("SELECT`Email` FROM `frat_users` WHERE 1"))]
    embed=discord.Embed(title='Is this correct?',description="Reply with y to send n to cancel",color=embed_color)
    embed.add_field(name='Subject',value=message_subject,inline=False)
    embed.add_field(name='Message Body',value=message_body,inline=False)
    embed.add_field(name='Emails to be sent to:',value=emails,inline=False)
    await ctx.author.send(embed=embed)
    if (await self.bot.wait_for('message',check=check)).content.lower() == 'y':
      send_mail(text = message_body,subject = message_subject, to_emails=emails)
      await ctx.author.send('Email Sent')
    else: 
      await ctx.author.send('Cancelled')


def setup(bot):
	bot.add_cog(EBlast(bot))


def send_mail(text='Email Body', subject='New E-Blast', from_email='AKPsi E-Blast <akpsieblast@gmail.com>', to_emails=None, html=None):
    assert isinstance(to_emails, list)
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject
    txt_part = MIMEText(text, 'plain')
    msg.attach(txt_part)
    if html != None:
        html_part = MIMEText(html, 'html')
        msg.attach(html_part)
    msg_str = msg.as_string()
    # login to my smtp server
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.ehlo()
    server.starttls()
    server.login(email, email_password)
    server.sendmail(from_email, to_emails, msg_str)
    server.quit()

