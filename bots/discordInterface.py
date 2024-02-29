import asyncio
from bots.defaultBot import DefaultBot
from helpers.gateHelper import GateHelper
from helpers.textsContainer import TextsContainer
import discord
from discord.ext import commands, tasks
from discord import app_commands

#TODO: fix texts send
texts = TextsContainer()

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


async def sendStart(additionalText, channel):
    fullText = texts.endText + additionalText
    await channel.send(fullText)

async def sendEnd(additionalText, channel):
    fullText = texts.startText + additionalText
    await channel.send(fullText)

async def sendStartMultiple(additionalText, channels):
    await asyncio.gather(*[sendStart(additionalText, channel) for channel in channels])

async def sendEndMultiple(additionalText, channels):
    await asyncio.gather(*[sendEnd(additionalText, channel) for channel in channels])


async def sendStartClear(channels):
    await sendStartMultiple('', channels)

async def sendEndClear(channels):
    await sendEndMultiple('', channels)

async def sendStartingIn(channels):
    await sendStartMultiple(texts.newText.format(GateHelper.toNextGateEventMin()), channels)

async def sendEndingIn(channels):
    await sendEndMultiple(texts.endingText.format(GateHelper.toNextGateEventMin()), channels)


async def sendCurrentStatus():
    global startChannels
    if GateHelper.isGateRunning():
        await sendStartClear(startChannels)
    else:
        await sendEndClear(startChannels)

async def sendStartedStatusChannel(channel):
    global startChannels
    if GateHelper.isGateRunning():
        await sendEndingIn([channel])
    else:
        await sendStartingIn([channel])


async def startTimer(ctx):
    global startChannels
    if ctx.channel in startChannels:
        await ctx.response.send_message("Already started")
        return
    print('Started dis channel!')
    channel = ctx.channel
    startChannels.append(channel)
    await ctx.response.send_message("Release the kraken!")
    await sendStartedStatusChannel(channel)

async def endTimer(ctx):
    global startChannels
    if not ctx.channel in startChannels:
        await ctx.response.send_message("Already stopped")
        return
    print('Stopped dis channel!')
    channel = ctx.channel
    startChannels.remove(channel)
    await ctx.response.send_message("Flood gates are closed")
    await sendStartedStatusChannel(channel)


class DisBot(DefaultBot):
    async def startBot(self):
        await bot.start(self.token)

    def _createBot(self):
        return
    
    async def sendStatus():
        await sendCurrentStatus()
        
