#Import Libs

import discord
import feedparser
from discord.ext import commands, tasks
from bs4 import BeautifulSoup
import credentials

#Define prefix to Bot
client = commands.Bot(command_prefix = '!', case_insensitive = True)

#Define RSS feed
NewsFeed = feedparser.parse(credentials.rss)
entry = NewsFeed.entries[0]

#Transform HTML to Normal Language
soup = BeautifulSoup(markup=entry.summary, features="lxml") 

#Defining variables its optional
titulo = entry.title
data = entry.published
link = entry.link

#Crate a loop
class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # an attribute we can access from our task
        self.counter = 0

        # start the task to run in the background
        self.noticias.start()

    async def on_ready(self):
        print('Estamos online!')
        print(self.user.name)
        print(self.user.id)
        print('------')

    @tasks.loop(minutes=60) # task runs every X seconds
    async def noticias(self):
        channel = self.get_channel(credentials.canal) # channel ID 
        self.counter += 1

        if entry.id != nnoticia:
            await channel.send('---------')
            await channel.send(data)
            await channel.send(titulo)
            await channel.send(soup.get_text())
            await channel.send('**------Link da noticia----**')
            await channel.send(link)

        else:
            print('Sem novas noticias')

     
    @noticias.before_loop
    async def before_my_task(self):
        await self.wait_until_ready() # wait for the bot to login

#Whenever the RSS id changes it will be relocated to the variable
nnoticia = entry.id

#Start this Bot
client = MyClient()
client.run(credentials.token) #Id do Bot
