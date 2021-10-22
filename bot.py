from discord.ext import commands
import discord
from datetime import datetime
from garf import garf
from random import choice
from os import getenv

apikey = getenv("apikey")
bot = commands.Bot(command_prefix="!ga")
footers = ["Feed me.", "Paws Inc., property of the SCP Foundation", "I'm not overweight, I'm undertall.", 'Diet is "die" with a "t".', "Anybody can exercise... But this kind of lethargy takes real discipline."]

@bot.command(pass_context=True, name="rf")
async def comic(ctx, *args):
   
    activeFooters = footers
    if datetime.now().weekday() == 0:
        activeFooters.append("Ugh... It's Monday...")
    else:
        activeFooters.append("I'm in a good mood... It's not Monday.")
       
    if len(args) == 1:
        args = args[0]
    
    filterdate = "".join(i for i in args if i.isnumeric())
    if len(filterdate) not in range(6, 9):
        raise Exception("InvalidDateFormat")
        
    garfDate = dateParser(filterdate)
    garfComic = garf(garfDate)
    print(garfComic.date)
    year, month, day = garfComic.date
    
    garfEmbed = discord.Embed(title="Garfield Comic on {}".format(garfComic.fullDate), url=garfComic.url, color=0xFCAA14)
    embedFooter = choice(activeFooters)
    
    garfEmbed.set_image(url=garfComic.url)
    garfEmbed.set_footer(text=embedFooter)
    
    await ctx.send(embed=garfEmbed)
    
@bot.command(pass_context=True, name="error")
@commands.is_owner()
async def triggerError(ctx, *args):
    print(ballsack)
    
@bot.event
async def on_command_error(ctx, e):
    
    exception = e.original
    exceptionCause = " ".join(i for i in exception.args)
    exceptionName = exception.__class__.__name__
    
    if exceptionName == "InvalidDateFormat":
        title = "Invalid Date Format"
        desc = "You entered a date in an invalid format. Make sure to type YEAR-MONTH-DAY\n```!garf 1995 07 29\n!garf 1995-07-29```\nfor July 29th, 1995."
        color = 0xFFFF00
    elif exceptionName == "InvalidDate":
        title = "Invalid Date"
        desc = "The date you entered doesn't have an associated Garfield comic!\n**If you entered today's date, the comic may not be out yet!**"
        color = 0xFFFF00
    else:
        title = "An Exception Occurred!"
        desc = f"See the error below:\n```{exceptionName}: {exceptionCause}```\nThis is a debug message. If you want to report this message to the bot dev, go to\nhttps://github.com/skippyaic/garfbot"
        color = 0xFF0000
    
    embed = discord.Embed(title=title, description=desc, color=color)
    await ctx.send(embed=embed)
    
def dateParser(date): ## str of only numbers, year, month, day (for example, 19950729)
    date = datetime.strptime(date, "%Y%m%d")
    zeroAdd = lambda x: "0" + str(x) if len(str(x)) == 1 else str(x)
    
    garfCompatDate = []
    for i in (date.year, date.month, date.day):
        newNumber = zeroAdd(i)
        garfCompatDate.append(newNumber)
    return garfCompatDate
    

bot.run(apikey)