import os

#These variables are for channels and roles
signup_id = 775539289500811304
new_mention_id = 772583438191689730
admin_roles = ("Founding Member","Founding Contributer")
tickets_category = 774332003621404763
suggestion_channel = 775753717952806913
covid_updates = 775810361847709767


#This is your discord bot token
token = os.environ.get('token')

#What color do you want for embeds?
embed_color = 0x15223d


#Database login info.
host=os.environ.get('host')
db_user=os.environ.get('db_user')
db_password=os.environ.get('db_password')
database=os.environ.get('database')

#Email Info
email = 'akpsieblast@gmail.com'
email_password = os.environ.get('email_password')
email_signature = 'This message was sent automatically by the discord bot please check the discord or reply to EMAIL YOU WANT HERE'


#Other API Tokens
weather_token = '00389432347e0b586478c8709f381c00'
MUSIC_TOKEN = '386e76f571fd03ac5e56501fe05db36a'