import discord
from actions import secrets
from actions.movie_tv_search import search
from actions.googleImages import imageSearch

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
        try:
            movieTitle, movieURL, movieThumbURL, moviePlot, movieRelease, movieScore, movieGenre = search(message.content)
            em = discord.Embed(title=movieTitle, url=movieURL, description=moviePlot, color=0xf3ce13)
            em.set_author(name="IMDb:", url="https://imdbpy.sourceforge.io/")
            em.add_field(name="Score", value=movieScore, inline=True)
            em.add_field(name="Release Date", value=movieRelease, inline=True)
            em.add_field(name="Genre(s)", value=movieGenre, inline=True)
            em.set_image(url=movieThumbURL)
            await client.send_message(message.channel, embed=em)
        except:
            em = discord.Embed(title="Cannot find movie", description="I could not find that movie in the IMDb database. Please try again with a different search", color=0xf3ce13)
            em.set_author(name="IMDb:", url="https://imdbpy.sourceforge.io/")
            await client.send_message(message.channel, embed=em)
    if message.content == (".help"):
        em = discord.Embed(title="Link to the commands used by the bot.", url="https://github.com/Patrick-G-W/discord-bot/blob/master/extra/help.md", color=0xE66000)
        await client.send_message(message.channel, embed=em)
    if message.content.startswith(".images"):
        try:
            em = discord.Embed(title="Google Image Search Result:", color=0x4286f4)
            em.set_image(url=imageSearch(message.content))
            await client.send_message(message.channel, embed=em)
        except:
            em = discord.Embed(title="Google Image Search Result:", description="Cannot find an image using the search terms provided. Try another search.", color=0x4286f4)
            await client.send_message(message.channel, embed=em)

client.run(secrets.TOKEN)

# embed help:
# https://cog-creators.github.io/discord-embed-sandbox/
