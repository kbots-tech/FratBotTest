"""Commands for the covid module"""
import discord
import requests
import numpy as np
import matplotlib.pyplot as plt
from discord.ext import commands
from bs4 import BeautifulSoup
from discord.ext import tasks
from setting import covid_updates, embed_color

from datetime import datetime

class CovidStats(commands.Cog,name='covid'):
    """commands for the covid finder"""
    def __init__(self, bot):
        self.bot = bot
        self.old_data = []

    @commands.command(
        name = "covidstats",
        brief = "returns covid dashboard stats",
    )
    async def covidstats(self,ctx):
      data = covid_data()
      embed = embed_generator(data)
      file = discord.File("plot.png", filename="image.png")
      embed.set_image(url="attachment://image.png")
      await ctx.send(file=file, embed=embed)
    
    @commands.Cog.listener()
    async def on_ready(self):
      print('starting task')
      self.check_stats.start()

    @tasks.loop(hours=1.0)
    async def check_stats(self):
      channel=self.bot.get_channel(covid_updates)
      new_data = covid_data()
      if new_data['num tests last week'] != self.old_data['num tests last week']:
        data_time = datetime.now()
        embed=embed_generator(new_data)
        embed.set_footer(text='Updated as of: '+str(data_time))
        file = discord.File("plot.png", filename="image.png")
        embed.set_image(url="attachment://image.png")
        print('sending update')
        await channel.send(file=file, embed=embed)
        self.old_data = new_data['num tests last week']
      else:
        print('no new data')

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    """sets up the cog"""
    bot.add_cog(CovidStats(bot))



def covid_data():
  url="https://www.bradley.edu/sites/coronavirus/dashboard/"

  html_content = requests.get(url).text

  soup = BeautifulSoup(html_content, 'html.parser')
  
  for script in soup.find_all("script"):
    try:
      if 'var chart' in script.string:
        chart_data = script.string
    except TypeError:
      pass
  
  pos_data = chart_data.split('dataPoints')[2].split(']',1)[0].split(',\n')

  test_data = chart_data.split('dataPoints: [',1)[1].split(']',1)[0].split(',\n')

  percent_data = chart_data.split('dataPoints')[3].split(': [')[1].split(']',1)[0].split(',\n')
    
  organized_data = {}  
  for count in range(0,len(test_data)-1):
    tests = test_data[count].replace('\n','').replace('\t','').replace(' ','')
    pos = pos_data[count].replace('\n','').replace('\t','').replace(' ','').replace(':[','')
    percent = percent_data[count].replace('\n','').replace('\t','').replace(' ','')

    try:
      organized_data[tests.split('"')[3]] = [tests[3:6],pos[3:4],percent[3:7]]
    except IndexError:
      pass

  labels = []
  tests_data = []
  pos_data = []
  per_data = []

  for value in organized_data:
    labels.append(str(value))
    tests_data.append(float(organized_data[value][0]))
    pos_data.append(float(organized_data[value][1]))
    per_data.append(float(organized_data[value][2].replace(',','')))

  x = np.arange(len(labels))  # the label locations
  width = 0.35  # the width of the bars

  fig, ax = plt.subplots()
  rects1 = ax.bar(x - width/2, tests_data, width, label='Total Tests',color='grey')
  rects2 = ax.bar(x + width/2, pos_data, width, label='Positive Tests',color='red')
  ax2 = ax.twinx()
  ax2.set_ylabel('Positivity Rate')
  ax2.set_ylim([0,40])
  ax.set_ylim([0,400])
  ax2.plot(labels,per_data,color='black')
  ax.grid(color='silver', linestyle='-', linewidth=.5,axis='y')
  ax.set_ylabel('Num Tests')
  ax.set_title('Covid Test Results')
  ax.set_xticks(x)
  ax.set_xticklabels(labels)
  ax.legend()

  for x,y in zip(labels,per_data):

    label = "{:.2f}".format(y)

    plt.annotate(label, # this is the text
                 (x,y), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center


  def autolabel(rects):
      """Attach a text label above each bar in *rects*, displaying its height."""
      for rect in rects:
          height = rect.get_height()
          ax.annotate('{}'.format(height),
                      xy=(rect.get_x() + rect.get_width() / 2, height),
                      xytext=(0, 3),  # 3 points vertical offset
                      textcoords="offset points",
                      ha='center', va='bottom'
                      )

  autolabel(rects1)
  autolabel(rects2)

  fig.tight_layout()
  
  plt.savefig('plot.png')

  data=(soup.get_text())
  data=data.split("COVID-19 Dashboard")[2]
  data=data.split("\n\n\n")
  final_data = {}
  final_data['title'] = soup.title.text
  final_data['recent days'] = data[1:6]
  final_data['num tests last week'] = data[7]
  final_data['positive last week'] = data[8]
  final_data['positivity rate last week'] = data[10]
  final_data['pending tests'] = data[12]
  final_data['total on campus positive'] = data[9]
  final_data['average positivity on campus'] = data[21]
  final_data['off campus positive last week'] = data[13]
  final_data['off campus positives'] = data[14]
  
  final_data['total tests'] = data[18]
  final_data['total positive last week'] = data[19]
  final_data['total positive'] = data[20]
  
  return final_data

def embed_generator(data):
      embed=discord.Embed(title=data['title'],url = 'https://www.bradley.edu/sites/coronavirus/dashboard/',description='**Recent Positive Tests (last week)**',color=embed_color)
      for values in data['recent days']:
        split = values.split('\n',3)
        if split[1]:
          embed.add_field(name=split[1],value=split[2]+'\n'+split[3],inline=True)
        elif split[2]:
          embed.add_field(name=split[2],value=split[3],inline=True)
      split = data['num tests last week'].split('\n',2)
      embed.add_field(name=split[1],value=split[2],inline=False)
      split = data['positive last week'].split('\n\n',2)
      embed.add_field(name=split[1],value=split[2],inline=False)
      split = data['positivity rate last week'].split('\n\n',2)
      embed.add_field(name=split[1],value=split[2],inline=False)
      split = data['pending tests'].split('\n\n',2)
      embed.add_field(name=split[0],value=split[1],inline=False)
      split = data['total tests'].split('\n\n',2)
      embed.add_field(name=split[0],value=split[1],inline=False)
      split = data['total on campus positive'].split('\n\n',2)
      embed.add_field(name=split[1],value=split[2],inline=False)
      split = data['average positivity on campus'].split('\n\n',2)
      embed.add_field(name=split[1],value=split[2],inline=False)
      split = data['off campus positive last week'].split('\n\n',2)
      embed.add_field(name=split[1],value=split[2],inline=False)
      split = data['off campus positives'].split('\n\n',2)
      embed.add_field(name=split[1],value=split[2],inline=False)
      split = data['total positive last week'].split('\n\n',2)
      embed.add_field(name=split[1],value=split[2],inline=False)
      split = data['total positive'].split('\n\n',2)
      embed.add_field(name=split[1],value=split[2],inline=False)
      return embed

