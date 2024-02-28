import os
import discord
import math
import asyncio
import atexit
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord import app_commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

startChannels = []

intents = discord.Intents.default()
#intents.presences = False
intents.messages = True
#TODO: add tts

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print('Connected to Discord!')
    
@bot.tree.command(name="start",description="Starts gates timers!")
async def _start(ctx):
    await startTimer(ctx)

@bot.tree.command(name="startgates",description="Starts gates timers!")
async def _startGates(ctx):
    await startTimer(ctx)

@bot.tree.command(name="stop",description="Stops gates timers!")
async def _stop(ctx):
    await endTimer(ctx)

@bot.tree.command(name="stopgates",description="Stops gates timers!")
async def _stopGates(ctx):
    await endTimer(ctx)

@bot.tree.command(name="gates",description="Starts gates timers!")
async def _gatesToggle(ctx):
    global startChannels
    if ctx.channel in startChannels:
         await endTimer(ctx)
    else:
        await startTimer(ctx)


async def startTimer(ctx):
    global startChannels
    if ctx.channel in startChannels:
        await ctx.response.send_message("Already started")
        return
    channel = ctx.channel
    startChannels.append(channel)
    await ctx.response.send_message("Release the kraken!")
    await sendStartBeforeChannel(channel)
    if not checkTimer.is_running():
        checkTimer.start()

async def endTimer(ctx):
    global startChannels
    if not ctx.channel in startChannels:
        await ctx.response.send_message("Already stopped")
        return
    channel = ctx.channel
    startChannels.remove(channel)
    await ctx.response.send_message("Flood gates are closed")
    await sendStartBeforeChannel(channel)
    if  len(startChannels) == 0:
        checkTimer.stop()

endText = 'Gate Ended!'
startText = 'Gate Started!'
newText = ' New in {} min'
endingText = ' Ending in {} min'
shutdownText = 'Sorry! Closing for now!'

async def sendStart(additionalText, channel):
    global startChannels
    fullText = startText + additionalText
    await channel.send(fullText)

async def sendEnd(additionalText, channel):
    global startChannels
    fullText = endText + additionalText
    await channel.send(fullText)

async def sendStartMultiple(additionalText, channels):
    for channel in channels:
        await sendStart(additionalText, channel)

async def sendEndMultiple(additionalText, channels):
    for channel in channels:
        await sendEnd(additionalText, channel)


async def sendStartClear(channels):
    await sendStartMultiple('', channels)

async def sendEndClear(channels):
    await sendEndMultiple('', channels)

async def sendStartingIn(channels):
    await sendStartMultiple(endingText.format(toNextGateEventMin()), channels)

async def sendEndingIn(channels):
    await sendEndMultiple(newText.format(toNextGateEventMin()), channels)



async def sendStartBeforeChannel(channel):
    if isGateRunning():
        await sendStartingIn([channel])
    else:
        await sendEndingIn([channel])

async def sendStartBeforeAll():
    if isGateRunning():
        await sendStartingIn(startChannels)
    else:
        await sendEndingIn(startChannels)

async def sendStatusClearAll():
    if isGateRunning():
        await sendStartClear(startChannels)
    else:
        await sendEndClear(startChannels)


@tasks.loop(minutes=10)
async def checkTimer():
    await endStatusClearAll()


def currentMinute() -> int:
    return datetime.now().minute

#gates are running minutes 0 to 10, 20 to 30, 40 to 50(only on odd minutes)
def isGateRunning() -> bool:
    return currentMinute() // 10 % 2 == 0

def toNextGateEventMin() -> int:
    return 10 - currentMinute() % 10

def nextTenMinStrippedToHour() -> datetime:
    now = datetime.now()
    neededDateTime = now + timedelta(minutes=toNextGateEventMin())
    return datetime(year=neededDateTime.year, month=neededDateTime.month, day=neededDateTime.day, hour=neededDateTime.hour, minute=neededDateTime.minute, second=1)

def toTextMin() -> int:
    return (nextTenMinStrippedToHour() - datetime.now()).seconds

@checkTimer.before_loop
async def beforeTimer():
    await bot.wait_until_ready()
    await asyncio.sleep(toTextMin())


#@atexit.register
#def exit_handler():
#    asyncio.new_event_loop().run_until_complete(sendCloseMessageToChats())
    
#async def sendCloseMessageToChats():
#    global startChannels
#    channels = [asyncio.create_task(channel.send(shutdownText)) for channel in startChannels]
#    await asyncio.wait(channels, return_when=asyncio.ALL_COMPLETED)


#async def main():
#    await bot.start(TOKEN)
#    await sendCloseMessageToChats()

#asyncio.run(main())
bot.run(TOKEN)
