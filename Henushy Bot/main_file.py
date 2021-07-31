
'''this loads the "DISCORD_TOKEN" string from the .env file'''

from discord import guild, message
from helpers import quick_embed
from logging import root
from dotenv import load_dotenv
import os
import random
import json
import math
from ahttp import HTTP
from helpers import quick_embed, pretty_dt
import threading

QUOTES = json.load(open("quotes.json"))


load_dotenv() 

TOKEN = os.environ["DISCORD_TOKEN"] 

import discord

from discord.ext import commands 

intents = discord.Intents.all() # will require all intents by default, change this to match your bot's intents

bot = commands.Bot(
                    command_prefix="-",
                    intents=intents,
                    #help_command=None # <- uncomment this if you want to write your own help command
                    )

requests = HTTP()

at_everyone = discord.AllowedMentions(everyone = True)

@bot.event # @bot.event attaches the function to the bot's event listener. 
async def on_ready(): #the name of the function denotes which event it listens to
    print(f"{bot.user.name} has connected to Discord!")

greetings = ("hello","hey","hola","hi")
sadlife = ("depressed","sad","sadge","lonely")
badwords = ['fuck', 'shit', 'dumb','dumbass','stupid','whore']

messageCount = {}

@bot.event
async def on_message(message : discord.Message):
    if message.author == bot.user: 
        return
    if any(greet in message.content for greet in greetings):
        await message.reply("hello " + str(message.author.display_name),mention_author=False)
    elif any(sadword in message.content for sadword in sadlife):
        await message.reply(str(bot.user.name) + " thinks you're depressed. Are you depressed?",mention_author = False)
 

    author = message.author
    if author.id in messageCount:
        messageCount[author.id] += 1
    else:
        if message.author != bot.user:
            messageCount[author.id] = 1

    for i in badwords: # Go through the list of bad words;
        if i in message.content:
            await message.delete()
            await message.channel.send(f"{message.author.mention} Don't use that word you donkey!")
            bot.dispatch('profanity', message, i)
            return # So that it doesn't try to delete the message again, which will cause an error.


    await bot.process_commands(message)


def printit():
    threading.Timer(2.0, printit).start()
    print (messageCount)

# printit()



#################Commands#################

'''@bot.command decorator adds this function as a command'''
@bot.command() 
async def return_info(ctx,content:str):  
    await ctx.send(content,mention_author=False) 

@bot.command()
async def peepee(ctx):
    size = "8" + (random.randint(1,19)*"=") + "D"
    await quick_embed(ctx,description=size,author={"name": ctx.author.name + "'s peepee size", "icon_url": ctx.author.avatar_url})

@bot.command()
async def inspire(ctx):
    randomnum = random.randint(0,200)
    the_quote = str(QUOTES[randomnum]["text"]) + '- ' + str(QUOTES[randomnum]["author"])
    await quick_embed(ctx,description=the_quote,author={"name": ctx.author.name + "'s inspirational quote", "icon_url": ctx.author.avatar_url})

@bot.command()
async def time(ctx, dt: float = 100):
    await quick_embed(ctx,description=f"```yaml\n {pretty_dt(dt)}```")

@bot.command()
async def numberfact(ctx, number: int):
    get_data = await requests.get_text(f"http://numbersapi.com/{number}/year?json")
    text = get_data["text"]
    await quick_embed(ctx,description=text,author={"name": f"You chose the number {number}"})

channel_names = ["general","General"]

@bot.command()
async def get_channel(ctx, given_name=None):
    for channel in ctx.guild.channels:
        if any(channel.name in given_name for channel.name in channel_names):
            wanted_channel_id = channel.id

    await ctx.send(wanted_channel_id)

@bot.command()
async def ping(ctx,channel_name = None):
    for channel in ctx.guild.channels:
        if channel.name == channel_name:
            id_needed = channel.id
            await bot.get_channel(id_needed).send(f"@everyone Welcome Brothers and Sisters ",allowed_mentions=at_everyone)

@bot.command()
async def messenger(ctx,person: discord.Member=None):
    member = person or ctx.author
    await quick_embed(ctx,description=f"{member} has typed {messageCount.get(member.id,0)} messages in the server",author={"name": f"Message Counter"})


################CALCULATOR################

def addbot(x: float,y: float):
    return x + y

def subtractbot(x: float,y: float):
    return x-y

def multiplybot(x: int,y: int):
    return float(x*y)

def dividebot(x: float, y: float):
    return x/y

def rootbot(x: float):
    return math.sqrt(x)

def sinbot(x: float):
    return math.sin(x)

def cosbot(x: float):
    return math.cos(x)

@bot.command()  
async def add(ctx,x: float, y:float):  
    await ctx.send(int(addbot(x,y)))

@bot.command()  
async def subtract(ctx,x: float, y:float):  
    await ctx.send(int(subtractbot(x,y)))

@bot.command()  
async def multiply(ctx,x: int,y: int):  
    await ctx.send(int(multiplybot(x,y)))

@bot.command()  
async def divide(ctx,x: float, y:float):  
    await ctx.send(int(dividebot(x,y)))

@bot.command()  
async def squareroot(ctx,x: float):  
    await ctx.send(round(rootbot(x),3))

@bot.command()  
async def sin(ctx,x: float):  
    await ctx.send((sinbot(x)))

@bot.command()  
async def cos(ctx,x: float):  
    await ctx.send((cosbot(x)))

bot.run(TOKEN) #runs a bot with the specified [TOKEN], this connects the wrapper to your bot 
