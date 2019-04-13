import discord
from actions import secrets
from actions.movie_tv_search import search
from actions.googleImages import imageSearch
from actions.database import createDatabase, insertNewUserIntoDatabase, removeRedundantUsers, updateDatabase

client = discord.Client()


@client.event
async def on_ready():
    print("Starting bot...")
    createDatabase(client.get_all_members())
    print("The bot is ready")
    await client.change_presence(activity=discord.Game(name=".help for commands"), status=".help for commands", afk=True)


@client.event
async def on_member_join(member):
    print("New member {0} found. Adding user to database.".format(member))
    insertNewUserIntoDatabase(member.id)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "Hello":
        await message.channel.send("World")
    if message.content.startswith(".imdb"):
        try:
            movieTitle, movieURL, movieThumbURL, moviePlot, movieRelease, movieScore, movieGenre = search(message.content)
            em = discord.Embed(title=movieTitle, url=movieURL, description=moviePlot, color=0xf3ce13)
            em.set_author(name="IMDb:", url="https://imdbpy.sourceforge.io/")
            em.add_field(name="Score", value=movieScore, inline=True)
            em.add_field(name="Release Date", value=movieRelease, inline=True)
            em.add_field(name="Genre(s)", value=movieGenre, inline=True)
            em.set_image(url=movieThumbURL)
            await message.channel.send(embed=em)
        except:
            em = discord.Embed(title="Cannot find movie", description="I could not find that movie in the IMDb \
            database. Please try again with a different search", color=0xFF0000)
            em.set_author(name="IMDb:", url="https://imdbpy.sourceforge.io/")
            await message.channel.send(embed=em)
    if message.content == ".help":
        for x in client.get_all_members():
            print(x.name + "#" + str(x.discriminator))
            if x.name + "#" + str(x.discriminator) == "ZefStyle#3091":
                print("ay")
        em = discord.Embed(title="Link to the commands used by the bot.", url="https://github.com/Patrick-G-W/discord-bot/blob/master/extra/help.md", color=0xE66000)
        await message.channel.send(embed=em)
    if message.content.startswith(".images"):
        try:
            em = discord.Embed(title="Google Image Search Result:", color=0x4286f4)
            em.set_image(url=imageSearch(message.content))
            await message.channel.send(embed=em)
        except:
            em = discord.Embed(title="Google Image Search Result:", description="Cannot find an image using the search\
             terms provided. Try another search.", color=0xFF0000)
            await message.channel.send(embed=em)
    if message.content.startswith(".dbremove"):
        try:
            user = message.content[10:]
            for x in client.get_all_members():
                if str(x.name + "#" + str(x.discriminator)) == user:
                    removeRedundantUsers(x.id, x.name)
            em = discord.Embed(title="{0} has been removed from the database.", description="User {0} has been removed \
            from the database, and all their points are gone. If they are still in the server when the bot restarts, \
            they will rejoin the database with all their points wiped.", color=0x008000)
            await message.channel.send(embed=em)
        except:
            em = discord.Embed(title="Cannot find user", description="I cannot find that user or they have already been\
             wiped from the database list. Make sure to use their name and discriminator, it is formatted like \
             <name>#<number>.", color=0xFF0000)
            await message.channel.send(embed=em)
    if message.content == ".dbupdate":
        try:
            updateDatabase(client.get_all_members())
            em = discord.Embed(title="Updated database", description="I successfully updated the users database.")
            await message.channel.send(embed=em)
        except:
            em = discord.Embed(title="Cannot update database", description="I could not update the database. Please\
             contact the server admin or check the console for more information.", color=0xFF0000)
            await message.channel.send(embed=em)


client.run(secrets.TOKEN)

# embed help:
# https://cog-creators.github.io/discord-embed-sandbox/
