import discord
from discord.ext import commands
from discord import Embed, Colour
import logging
from dotenv import load_dotenv
import os
import random
import asyncio

# flask
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()
#--------------------------------------------------
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w' )
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

#---------------------------------------------------------------------------------------------------------
#     GACHA
#---------------------------------------------------------------------------------------------------------

gacha_list = ["100 years of good luck", "Piece of Dust" , "10000 ROCKS",
"A WILD TAKO" , "KAMALASAN HANGGANG SECOND LIFE"]

for i in range(30):
    print(random.choice(gacha_list))

#list of GIF

welcome_gif = [
    "https://i.pinimg.com/originals/d6/f2/d0/d6f2d0743b277ad2501acab9ecccfff3.gif",
    "https://giffiles.alphacoders.com/186/186797.gif",
    "https://64.media.tumblr.com/3a0b9c063235ba08654542c033b5f167/tumblr_oq3t31OrzH1rgyzl8o1_540.gifv",
    "https://64.media.tumblr.com/565088cc68d5c8dc42092cebfd10e9c8/37758b52062abb2b-b8/s540x810/a1705db951d0faa7445c915ddd6701cd2995868f.gif"
]

farewell_gif = [
    "https://gifdb.com/images/thumbnail/hanako-kun-teary-eyes-bye-bye-ln5mjwhemwdfjljt.gif",
    "https://68.media.tumblr.com/tumblr_mbsq3gnG611rzl82po1_500.gif",
    "https://www.gif-vif.com/trending/hayato-yuzuki-money-goes-bye-bye.gif",
    "https://www.mondieu.nu/adore/wp-content/uploads/2019/01/bye.gif",
]



#---------------------------------------------------------------------------------------------------------
#      Bot-Events
#---------------------------------------------------------------------------------------------------------

@bot.event
async def on_ready():
    print("I'm Readyyy")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content.lower()

    if "hello ruriko" in msg:
        await message.channel.send(f"konnichiwa {message.author.mention}! How have you been")

    elif any(word in msg for word in ["fine", "okay", "good", "alright"]):
        await message.channel.send("I'm glad to hear that! 🌸")

    await bot.process_commands(message)

#Member JOIN
@bot.event
async def on_member_join(member):
    channel_id = 1435246013781901317
    channel = bot.get_channel(channel_id)

    if channel:
        random_gif_welcome = random.choice(welcome_gif)

        embed = Embed(
            title = "Welcome ~ 🌸",
            description=(
                f"よろしくお願いします{member.mention} ! Hope you enjoy your stay here ✧｡٩(ˊᗜˋ )و✧*｡"
        ),
        colour=Colour.from_rgb(255, 153, 204)
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url=random_gif_welcome)
        await channel.send(embed=embed)

#Member LEAVE
@bot.event
async def on_member_remove(member):
    channel_id = 1435246013781901317
    channel = bot.get_channel(channel_id)

    if channel:
        random_gif_bye = random.choice(farewell_gif)

        embed = Embed(
            title = "Farewell ~ 🌸",
            description=(
                f"またね **{member.name}** ｡°(°¯᷄◠¯᷅°)°｡"
        ),
        colour=Colour.from_rgb(255, 153, 204)
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url=random_gif_bye)
        await channel.send(embed=embed)




#---------------------------------------------------------------------------------------------------------
#      Bot-Commands
#---------------------------------------------------------------------------------------------------------

#!hello
@bot.command()
async def hello(ctx):
    await ctx.send(f"Konnichiwa {ctx.author.mention}! gacha gacha gacha? ")

#!gacha
@bot.command()
async def gacha(ctx):
    roll_message = await ctx.send(f"🎰 Rolling the gacha for {ctx.author.mention}...")
    
    final_item = None  # prepare variable

    for i in range(5):  # simulate spins
        final_item = random.choice(gacha_list)
        await roll_message.edit(content=f"✨ Rolling... {final_item} ✨")
        await asyncio.sleep(1)  # add small delay (1 sec looks nice)

    # use the *last rolled item* as the final result
    await roll_message.edit(content=f"🎉 Wow {ctx.author.mention}, you got **{final_item}**! 🎉")


bot.run(token, log_handler=handler, log_level=logging.DEBUG)






