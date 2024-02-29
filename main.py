import os
import asyncio
import enum
from helpers.timer import Timer
from helpers.gateHelper import GateHelper
from helpers.textsContainer import TextsContainer
from bots.discordInterface import DisBot
#from bots.tgInterface import TGBot
from dotenv import load_dotenv

class Channels(enum.Enum):
    tg = 1
    dis = 2


load_dotenv()
DIS_TOKEN = os.getenv('DISCORD_TOKEN')
TG_TOKEN = os.getenv('TG_TOKEN')


if DIS_TOKEN is not None:
    disBot = DisBot(DIS_TOKEN, TextsContainer)
#if TG_TOKEN is not None:
    #tgBot = TGBot(TG_TOKEN, TextsContainer)


async def startTimer():
    if not checkTimer.is_running():
        checkTimer.start()

async def endTimer():
    currentUsers = 0
    if DIS_TOKEN is not None:
        currentUsers += disBot.currentUsers
    #if TG_TOKEN is not None:
        #currentUsers += tgBot.currentUsers
    if currentUsers == 0:
        checkTimer.stop()



async def checkTimer():
    await sendStatusToAll()

async def beforeTimer():
#    await bot.wait_until_ready()
    await asyncio.sleep(GateHelper.toTextMin())


async def sendStatusToAll():
    tasks = []
    if DIS_TOKEN is not None:
        tasks.append(disBot.sendStatus())
    #if TG_TOKEN is not None:
        #tasks.append(tgBot.sendStatus())
    await asyncio.gather(*tasks)


async def main():
    timer = Timer(GateHelper.minuteInterval, checkTimer, beforeTimer)
    tasks = [timer.asyncStart()]
    if DIS_TOKEN is not None:
        tasks.append(disBot.startBot())
    #if TG_TOKEN is not None:
        #tasks.append(tgBot.startBot)
    await asyncio.gather(*tasks)
    print("Finished")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt as e:
        print("Caught keyboard interrupt. Canceling tasks...")
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()