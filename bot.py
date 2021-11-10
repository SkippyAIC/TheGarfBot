"""
MIT License

Copyright (c) 2021 SkippyAIC
Copyright (c) 2015-present Rapptz - discord.py

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


from discord.ext import commands
import discord
from datetime import datetime
from garf import garf
from random import choice, randint
from os import getenv




## The bot natively runs in US Eastern timezone, if you are in another timezone it is heavily recommended to install the pytz library and set it to US Eastern.




apikey = getenv("apikey")
bot = commands.Bot(command_prefix="!ga", help_command=None)
footers = ["Feed me.", "Paws Inc., property of the SCP Foundation", "I'm not overweight, I'm undertall.", 'Diet is "die" with a "t".', "Anybody can exercise... But this kind of lethargy takes real discipline."]

@bot.command(pass_context=True, name="rf")
async def comic(ctx, *args):
    
    ## Determines Monday footer depending on whatever local timezone this script is being run in.
    activeFooters = footers
    if datetime.now().weekday() == 0:
        activeFooters.append("Ugh... It's Monday...")
    else:
        activeFooters.append("I'm in a good mood... It's not Monday.")
    
    ## If "today" is in given arguments, override with datetime.today() (or if tomorrow is in there, send THE COKE.)
    for i in args:
        if i.lower() == "today":
            ## Gets Garfield comic from current date, should be in US Eastern timezone, ideally.
            currentDate = datetime.today()
            args = (str(currentDate.year), str(currentDate.month), str(currentDate.day))
        elif i.lower() == "random":
            ## Gets a random date from 1979 to 2020, a lot of limits here to ensure a proper date is picked without having to do extra processing.
            randomYear, randomMonth, randomDay = str(randint(1979, 2020)), str(randint(1, 12)), str(randint(1, 28))
            args = (randomYear, randomMonth, randomDay)
        elif i.lower() == "tomorrow":
            await ctx.send(r"https://cdn.discordapp.com/attachments/290667374468661249/891899409841926164/E_2j7DSVEAcccsa.png")
            return
        
    ## Normalizes list and sends to garf.py.
    comicDate = garfDate(args)
    garfComic = garf(comicDate)
    
    garfEmbed = discord.Embed(title="Garfield Comic on {}".format(garfComic.fullDate), url=garfComic.url, color=0xFCAA14)
    embedFooter = choice(activeFooters)
    
    garfEmbed.set_image(url=garfComic.url)
    garfEmbed.set_footer(text=embedFooter)
    
    await ctx.send(embed=garfEmbed)
    
    
@bot.command(pass_context=True)
async def help(ctx):
    
    helpEmbed = discord.Embed(title="GarfBot Help", color=0xFCAA14)
    helpEmbed.add_field(name="!garf", value="*Takes one date*\nDisplays a Garfield comic from a certain date.\n**For Example:**\n``!garf 1995 07 29``")
    helpEmbed.add_field(name="!garf today", value="*Takes no arguments*\nDisplays the Garfield comic from today, in relation to US Eastern timezone.")
    helpEmbed.add_field(name="!garf random", value="*Takes no arguments*\nDisplays a random Garfield comic.")
    helpEmbed.set_image(url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.d-FOOBt6822ipWg-NKW6TwHaEo%26pid%3DApi&f=1")
    helpEmbed.set_footer(text="This bot pulls URLs from ucomics and has the user's client display them. Any connection error may be as a result of the user's connection to Discord, a hardware issue, or a ucomics site issue.")
    await ctx.send(embed=helpEmbed)

@bot.command(pass_context=True, name="error")
@commands.is_owner()
async def triggerError(ctx, *args):
    ## Intentional NameError, can only be triggered by the bot owner.
    print(test)
    
@bot.event
async def on_command_error(ctx, e):
    
    ## Discord.py does not give the original Exception object, so it must be retrieved. Also, @commands.is_owner() returns the Exception "NotOwner", which does not have a .original property.
    ## If a user attempts to use an owner-only command, an AttributeError Exception will occur. This is normal, and can be silenced with an if statement.
    exception = e.original
    
    ## Custom exceptions like InvalidDateFormat and InvalidDate do not derive from BaseException, so the Exception name would be stored in Exception.args. Otherwise, the name would be stored in Exception.__class__.__name__.
    exceptionName = exception.__class__.__name__
    exceptionCause = " ".join(i for i in exception.args)
    
    if "InvalidDateFormat" in exceptionCause:
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
    

bot.run(apikey)
