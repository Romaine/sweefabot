import discord
import asyncio
import os
import json

from discord.ext import commands
from mlgvoice import download
from replies import replies
from subprocess import call

token = os.environ['token']
description = "The most MLG bot in the world"
bot = commands.Bot(command_prefix='/', description=description)
tts_dict = json.load(open("tts_dict.json", "r"))
tts_params = []


@bot.command()
async def say(*text):
    await _say(*text)


async def _say(*text):
    if hasattr(bot, "player"):
        bot.player.pause()
    mp3 = download(" ".join(text), *tts_params)
    player = bot.voice.create_ffmpeg_player(mp3)
    player.start()


@bot.command()
async def arabs():
    word = "arabs"
    await _say(word.replace("s", "th").replace("r", "w"))


@bot.command()
async def lisp(*text):
    await _say(*[word.replace("s", "th").replace("r", "w") for word in text])


@bot.command()
async def restart():
    await call(["heroku", "ps:restart"])


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

async def yt(*args):
    await youtube(*args)




@bot.command()
async def TTS(*args):
    if len(args[0]):
        if args[0] == "set":
            pass
        elif args[0] in ["list", "l"]:
            if len(args) >= 2:
                if args[0] in tts_dict.keys():
                    print(tts_dict[args[0]])
            else:
                for i, lang in tts_dict.items():
                    print(i, lang[0])
                    bot.send_message(bot., " ".join([i, lang]))


@bot.event
async def on_voice_state_update(before, after):
    pass #if after


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    if not discord.opus.is_loaded():
        discord.opus.load_opus("/app/.heroku/vendor/lib/libopus.so")

    channel = bot.get_channel('327111755547279381')
    bot.voice = await bot.join_voice_channel(channel)

bot.run(token)
