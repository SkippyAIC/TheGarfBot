"""
MIT License

Copyright (c) 2021 SkippyAIC - TheGarfBot
Copyright (c) 2015-present Rapptz - discord.py
Copyright (c) 2020-2021 eunwoo1104 - discord-interactions

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


## REPLIT SET THIS PROJECT TO BASH *deafening screaming :)*


from discord.ext import commands
import discord
from discord_slash import SlashCommand, SlashContext
from garf import garf
from datetime import datetime
from random import choice, randint
from os import getenv
import pytz
##from keepAlive import keep_alive


apikey = getenv("apikey")
bot = discord.Client(intents=discord.Intents.default())
slash = SlashCommand(bot, sync_commands=True)
footers = ["Feed me.", "Paws Inc., property of the SCP Foundation", "I'm not overweight, I'm undertall.", 'Diet is "die" with a "t".', "Anybody can exercise... But this kind of lethargy takes real discipline."]
timez = pytz.timezone("America/New_York")

@bot.event
async def on_ready():
    ## Changes bot activity
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="The Garfield Show! !gahelp"))

@slash.slash(name="garf", description="Grab a Garfield comic from any date")
@commands.cooldown(1, 5, commands.BucketType.user)
async def comic(ctx, date):
    
    await ctx.defer()
    
    ## This allows for filtering of a string into a list by 3 non-numeric characters (whitespace, - / \) for maximum compatibility
    if date.lower() not in ("today", "random", "tomorrow"):
        for i in (" ", "-", "/", "\\"):
          newArgs = date.split(i)
          if len(newArgs) != 1:
            date = newArgs
            break
          elif i == "\\":
            raise Exception("InvalidDateFormat")
          else:
            continue
    else:
        date = [date]

    currentDate = datetime.now(tz=timez)
    
    ## Determines Monday footer depending on whatever local timezone this script is being run in.

    activeFooters = footers
    if currentDate.weekday() == 0:
        activeFooters.append("Ugh... It's Monday...")
    else:
        activeFooters.append("I'm in a good mood... It's not Monday.")
    
    ## If "today" is in given arguments, override with datetime.today() (or if tomorrow is in there, send THE COKE.)

    for i in date:
        if i.lower() == "today":
            ## Gets Garfield comic from current date, should be in US Eastern timezone, ideally.
            date = (str(currentDate.year), str(currentDate.month), str(currentDate.day))
        elif i.lower() == "random":
            ## Gets a random date from 1979 to 2020, a lot of limits here to ensure a proper date is picked without having to do extra processing.
            randomYear, randomMonth, randomDay = str(randint(1979, 2020)), str(randint(1, 12)), str(randint(1, 28))
            date = (randomYear, randomMonth, randomDay)
        elif i.lower() == "tomorrow":
            await ctx.send(r"https://cdn.discordapp.com/attachments/290667374468661249/891899409841926164/E_2j7DSVEAcccsa.png")
            return
        
    ## Normalizes list and sends to garf.py.

    comicDate = garfDate(date)
    garfComic = garf(comicDate)
    
    ## Creates embed for the comic

    garfEmbed = discord.Embed(title="Garfield Comic on {}".format(garfComic.fullDate), url=garfComic.url, color=0xFCAA14)
    embedFooter = choice(activeFooters)
    
    garfEmbed.set_image(url=garfComic.url)
    garfEmbed.set_footer(text=embedFooter)
    
    await ctx.send(embed=garfEmbed)
    
@slash.slash(name="help", description="TheGarfBot Help")
@commands.cooldown(1, 5, commands.BucketType.user)
async def help(ctx):
    helpEmbed = discord.Embed(title="TheGarfBot Help", color=0xFCAA14)
    helpEmbed.add_field(name="/garf", value="*Takes one date*\nDisplays a Garfield comic from a certain date.\n**For Example:**\n``/garf 1995 07 29``")
    helpEmbed.add_field(name="/garf today", value="*Takes no arguments*\nDisplays the Garfield comic from today, in relation to US Eastern timezone.")
    helpEmbed.add_field(name="/garf random", value="*Takes no arguments*\nDisplays a random Garfield comic.")
    helpEmbed.set_image(url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.d-FOOBt6822ipWg-NKW6TwHaEo%26pid%3DApi&f=1")
    helpEmbed.set_footer(text="Created by Skippy.aic. Licensed under the MIT License\nThis bot pulls URLs from ucomics and has the user's client display them. Any embed error may be as a result of the user's connection to Discord or a ucomics site issue.")
    await ctx.send(embed=helpEmbed)
    
@bot.event
async def on_slash_command_error(ctx, e):

    ## Custom exceptions like InvalidDateFormat and InvalidDate do not derive from BaseException, so the Exception name would be stored in Exception.args. Otherwise, the name would be stored in Exception.__class__.__name__.
    exceptionName = e.__class__.__name__
    exceptionCause = " ".join(i for i in e.args)
    
    if isinstance(e, commands.CommandOnCooldown):
        title = "You are on cooldown!"
        desc = "Hold up! You gotta wait **{}** more seconds before you can use another command.".format(int(e.retry_after))
        color = 0xFCAA14
    elif "InvalidDateFormat" in exceptionCause:
        title = "Invalid Date Format"
        desc = "You entered a date in an invalid format. Make sure to type YEAR-MONTH-DAY\n**For Example:**```!garf 1995 07 29\n!garf 1995-07-29```\nfor July 29th, 1995."
        color = 0xFFFF00
    elif "InvalidDate" in exceptionCause:
        title = "Invalid Date"
        desc = "The date you entered doesn't have an associated Garfield comic!\n**If you entered today's date, the comic may not be out yet!**"
        color = 0xFFFF00
    else:
        title = "An Exception Occurred!"
        desc = "See the error below:\n```{}: {}```\nThis is a debug message. If you want to report this message to the bot dev, go to\nhttps://github.com/skippyaic/garfbot".format(exceptionName, exceptionCause)
        color = 0xFF0000
    
    embed = discord.Embed(title=title, description=desc, color=color)
    await ctx.send(embed=embed)
    
def garfDate(date):
    ## Converts date tuple/list to string to be converted to datetime object to help discern year, month, and day.
    dateString = "".join(i for i in date if i.isnumeric())
    print(date)
    try:
        date = datetime.strptime(dateString, "%Y%m%d")
    except ValueError:
        raise Exception("InvalidDateFormat")
    zeroAdd = lambda x: "0" + str(x) if len(str(x)) == 1 else str(x)
    
    ## For year, month, and day in datetime object, add a zero to the beginning if needed, then append to a new list to be sent to the garf.py script.
    garfCompatDate = []
    for i in (date.year, date.month, date.day):
        newNumber = zeroAdd(i)
        garfCompatDate.append(newNumber)
    return garfCompatDate
    
##keep_alive()
bot.run(apikey)
