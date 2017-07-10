import discord
import asyncio

from auth import token
from discord.ext import commands
from mlgvoice import download
from replies import replies


description = "The most MLG bot in the world"
bot = commands.Bot(command_prefix='/', description=description)


@bot.command()
async def say(*text):
    await _say(text)


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
    for state in replies.keys():
        before_state = getattr(before, state)
        after_state = getattr(after, state)
        if before_state != after_state:
            if state == "mute":
                await _say(replies["deaf" if state.deaf else "mute"][after_state].format(after.display_name))
                break
            elif state == "self_mute":
                await _say(replies["self_deaf" if "self_deaf" else "self_mute"][after_state].format(after.display_name))
                break
            else:
                await _say(replies[state][after_state].format(after.display_name))
                break

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    channel = bot.get_channel('314489891859726347')
    bot.voice = await bot.join_voice_channel(channel)

bot.run(token)
