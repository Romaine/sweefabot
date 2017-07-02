import discord
import asyncio

from auth import token
from discord.ext import commands

from mlgvoice import download


description = "The most MLG bot in the world"
bot = commands.Bot(command_prefix='/', description=description)


@bot.command()
async def say(text):
    mp3 = download(
        text=text,
        engine=6,
        language=1,
        voice=5,
    )
    player = bot.voice.create_ffmpeg_player(mp3)
    player.start()


@bot.command()
async def youtube(*args):
    if args[0] == "stop":
        bot.player.stop()
    else:
        link = args[0]
        bot.player = await bot.voice.create_ytdl_player(link)
        bot.player.start()


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    channel = bot.get_channel('314489891859726347')
    bot.voice = await bot.join_voice_channel(channel)

bot.run(token)
