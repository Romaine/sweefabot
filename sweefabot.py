import discord
import asyncio
import os

from discord.ext import commands
from mlgvoice import download
from replies import replies
from ctypes.util import find_library


# token = os.environ.get('token')
token = "MzI2NjY0NzcwOTY1MjA5MDg4.DIIQ-w.WIhkQq9DAarRhjzCAMji5TEUzvw"
description = "The most MLG bot in the world"
bot = commands.Bot(command_prefix='/', description=description)



@bot.command()
async def say(*text):
    await _say(*text)


@bot.command()
async def arabs():
    word = "arabs"
    await _say(word.replace("s", "th").replace("r", "w"))


@bot.command()
async def lisp(*text):
    await _say(*[word.replace("s", "th").replace("r", "w") for word in text])


async def _say(*text):
    if hasattr(bot, "player"):
        bot.player.pause()
    mp3 = download(" ".join(text), 4, 1, 5)
    player = bot.voice.create_ffmpeg_player(mp3)
    player.start()


@bot.command()
async def youtube(*args):

    if args[0] == "stop":
        bot.player.stop()
    else:
        link = args[0]
        if hasattr(bot, "player"):
            bot.player.stop()
        bot.player = await bot.voice.create_ytdl_player(link)
        bot.player.start()

@bot.event
async def on_voice_state_update(before, after):
    pass#if after

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    if not discord.opus.is_loaded():
        discord.opus.load_opus(find_library("opus"))

    channel = bot.get_channel('314489891859726347')
    bot.voice = await bot.join_voice_channel(channel)

bot.run(token)
