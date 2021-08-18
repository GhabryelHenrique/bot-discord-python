#Import Libs
import discord
from discord.ext import commands, tasks
import credentials
import sopa
from bs4 import BeautifulSoup
import feedparser
import datetime
import locale

intents = discord.Intents.default()
intents.members = True

#Define prefix to Bot
client = commands.Bot(command_prefix = '!', case_insensitive = True, intents=intents)

#Crate a loop
class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # an attribute we can access from our task
        self.counter = 1

        # start the task to run in the background
        self.noticias.start()

    async def on_ready(self):
        channel1 = self.get_channel(credentials.log)
        await channel1.send('Estamos online!')

    @tasks.loop(minutes=60) # task runs every X seconds
    async def noticias(self):
        channel = self.get_channel(credentials.canal)
        channel1 = self.get_channel(credentials.log) # channel ID

        #Set to RSS
        NewsFeed = feedparser.parse(credentials.rss)
        entry = NewsFeed.entries[0]
        
        #Translate to HTML to normal language
        soup = BeautifulSoup(markup=entry.summary, features="lxml")

        #set variable (optional)
        titulo = entry.title
        data = entry.published[:-6]
        link = entry.link
        texto = soup.get_text()[:-51]
        await channel1.send('RSS Atualizado!')
        print('RSS Atualizado!')

        await channel.send('**---------**')
        await channel.send(data)
        await channel.send(titulo)
        await channel.send('-')
        await channel.send(texto)
        await channel.send('**----Link da noticia----**')
        await channel.send(link)
        await channel1.send('Noticia Enviada!')
        print('Noticia Enviada!')
     
    @noticias.before_loop
    async def before_my_task(self):
        await self.wait_until_ready() # wait for the bot to login

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!Hellow'):
            await message.reply('Hellow!', mention_author=True)

#Start this Bot
client = MyClient()
client.run(credentials.token) #Bot ID
