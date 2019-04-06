import discord
from actions import secrets
from actions.movie_tv_search import search
from actions.googleImages import *

client = discord.Client()

@client.event
async def on_ready():
    print("The bot is ready")
    await client.change_presence(game=discord.Game(name=".help for commands"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "Hello":
        await client.send_message(message.channel, "World")
    if message.content.startswith(".imdb"):
        #try:
        movieTitle, movieURL, movieThumbURL, moviePlot, movieRelease, movieScore, movieGenre = search(message.content)
        em = discord.Embed(title=movieTitle, url=movieURL, description=moviePlot, color=0xf3ce13)
        em.set_author(name="IMDb:", url="https://imdbpy.sourceforge.io/")
        em.add_field(name="Score", value=movieScore, inline=True)
        em.add_field(name="Release Date", value=movieRelease, inline=True)
        em.add_field(name="Genre(s)", value=movieGenre, inline=True)
        em.set_image(url=movieThumbURL)
        await client.send_message(message.channel, embed=em)
        #except:
            #await client.send_message(message.channel, "Cannot find movie")
    if message.content.startswith("test"):
        em = discord.Embed(title="Title", description="Description", color=0xDEADBF)
        em.set_author(name="Someone", icon_url=client.user.default_avatar_url)
        em.set_image(url="https://m.media-amazon.com/images/M/MV5BZDc2NGZiZDMtYjg3Ni00ZDhkLThlYWEtMzQwMDBlZDQzOWQ2XkEyXkFqcGdeQXVyNjc3OTE4Nzk@._V1_SY150_CR2,0,101,150_.jpg") # SET IMAGE
        await client.send_message(message.channel, embed=em)
    if message.content == (".help"):
        em = discord.Embed(title="Link to the commands used by the bot.", url="https://github.com/Patrick-G-W/discord-bot/blob/master/extra/help.md", color=0xE66000)
        await client.send_message(message.channel, embed=em)
    if message.content.startswith(".images"):
        await client.send_message(message.channel, paths)

client.run(secrets.TOKEN)

# embed help:
# https://cog-creators.github.io/discord-embed-sandbox/
