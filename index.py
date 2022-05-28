#Import Libs
import discord
from discord.ext import commands, tasks
import credentials
from bs4 import BeautifulSoup
import feedparser
from datetime import datetime, timedelta
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

        #transform HTML to normal language
        NewsFeed = feedparser.parse(credentials.rss)
        entry = NewsFeed.entries[0]
        soup = BeautifulSoup(markup=entry.summary, features="lxml")

        #trasform data to format Brazilian and UTC-3
        date_NewsFeed = datetime.strptime(entry.published[5:-6], "%d %b %Y %H:%M:%S") + timedelta(hours = -3)
        locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
        date_pt_BR = date_NewsFeed.strftime('%A, %d %b %Y %H:%M:%S')

        #Define variables (opitional)
        title = entry.title
        data = date_pt_BR
        link = entry.link
        text = soup.get_text()[:2000] #The discord is limited to 2000 characters per message, if you don't put this limitation the bot returns an error
        
        #Confirm to RSS is Ready
        await channel1.send('RSS Ready!')
        print('RSS Atualizado!')

        #If there is an error in the text, there is this redundancy system
        try:
            await channel.send(data)
            await channel.send(title)
            await channel.send('.')
            await channel.send(text)
            await channel.send('__**Read more at:**__')
            await channel.send(link)
            await channel1.send('News Sent Successfully')
            print('News Sent Successfully!')

        except:
            await channel.send('__**Não foi possivel escrever a noticia. Em breve tentaremos novamente**__')
            await channel1.send('Noticia não enviada')
            print('Noticia not sent')
     
    @noticias.before_loop
    async def before_my_task(self):
        await self.wait_until_ready() # wait for the bot to login

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!Hello'):
            await message.reply('Hello!', mention_author=True)

#Start this Bot
client = MyClient()
client.run(credentials.token) #Bot ID
