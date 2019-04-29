import discord
from actions import secrets
from actions.movie_tv_search import search
from actions.googleImages import imageSearch
from actions.database import createDatabase, insertNewUserIntoDatabase, removeRedundantUsers, updateDatabase, givePoints, removePoints, onMessageAddPoints, lookupUser

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
    roles = ', '.join(str(e) for e in member.roles)
    insertNewUserIntoDatabase(member.id, str(member.joined_at)[:23], member.avatar_url, roles, member.name)

@client.event
async def on_member_remove(member):
    return[]

@client.event
async def on_user_update(before, after):
    try:
        print("User change detected, updating user database...")
        updateDatabase(client.get_all_members())
        print("Updated user database.")
    except:
        print("Tried to update user database, couldn't. Check this console.")



@client.event
async def on_message(message):
    pointUser = str(message.author)
    for z in client.get_all_members():
        if (z.name + "#" + z.discriminator) == pointUser:
            onMessageAddPoints(z.id)

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
            userSplit = user.split('"')
            try:
                userDisc = userSplit[1]
            except IndexError:
                em = discord.Embed(title="Formatting error", description='Correct formatting: \n`.dbremove \
                "username#descriminator"`\ne.g. `.dbremove "alpha#1234"`\nYou can find a users\
                username and discriminator by clicking on the users profile, it is positioned below the users \
                server nickname.', color=0xFF0000)
                await message.channel.send(embed=em)
            if "#" not in userDisc:
                print("Error: Use username and discriminator when using this function.")
                em = discord.Embed(title="Formatting error", description='Correct formatting: \n`.dbremove \
                "username#descriminator"`\ne.g. `.dbremove "alpha#1234"`\nYou can find a users\
                username and discriminator by clicking on the users profile, it is positioned below the users \
                server nickname.', color=0xFF0000)
                await message.channel.send(embed=em)
            else:
                for x in client.get_all_members():
                    if str(x.name + "#" + str(x.discriminator)) == userDisc:
                        removeRedundantUsers(x.id, x.name)
                em = discord.Embed(title="{0} has been removed from the database.".format(userDisc), description="User {0}\
                 has been removed from the database, and all their points are gone. If they are still in the server when \
                 the bot restarts, they will rejoin the database with all their points \
                 wiped.".format(userDisc), color=0x008000)
                await message.channel.send(embed=em)
        except:
            em = discord.Embed(title="Cannot find user", description="I cannot find that user or they have already been\
             wiped from the database list. Make sure to use their name and discriminator, it is formatted like \
             <name>#<number>.", color=0xFF0000)
            await message.channel.send(embed=em)

    if message.content == ".dbupdate":
        try:
            updateDatabase(client.get_all_members())
            em = discord.Embed(title="Updated database", description="I successfully updated the users database.", \
                               color=0x008000)
            await message.channel.send(embed=em)
        except:
            em = discord.Embed(title="Cannot update database", description="I could not update the database. Please\
             contact the server admin or check the console for more information.", color=0xFF0000)
            await message.channel.send(embed=em)

    if message.content.startswith(".givepoints"):
        try:
            if message.author.permissions_in(message.channel).administrator:
                user = message.content[12:]
                userSplit = user.split('"')
                try:
                    userDisc = userSplit[1]
                except IndexError:
                    em = discord.Embed(title="Formatting error", description='Correct formatting: \n`.givepoints \
                    "username#descriminator" points`\ne.g. `.givepoints "alpha#1234" 100`\nYou can find a users\
                    username and discriminator by clicking on the users profile, it is positioned below the users \
                    server nickname.', color=0xFF0000)
                    await message.channel.send(embed=em)
                points = userSplit[2]
                print(userSplit)
                if "#" not in userDisc or points is not points.isdigit():
                    print("Error: Use username and discriminator when using this function.")
                    em = discord.Embed(title="Formatting error", description='Correct formatting: \n`.givepoints \
                    "username#descriminator" points`\ne.g. `.givepoints "alpha#1234" 100`\nYou can find a users\
                    username and discriminator by clicking on the users profile, it is positioned below the users \
                    server nickname.', color=0xFF0000)
                    await message.channel.send(embed=em)
                else:
                    for x in client.get_all_members():
                        if (x.name + "#" + x.discriminator) == userDisc:
                            givePoints(x.id, points)
                            em = discord.Embed(title="Successfully gave points.", description="I have given {0} \
                            points to {1}.".format(points, userDisc), color=0x008000)
                            await message.channel.send(embed=em)
        except:
            user = message.content[12:]
            userSplit = user.split('"')
            userDisc = userSplit[1]
            points = userSplit[2]
            em = discord.Embed(title="Could not give points.", description="Could not give {0} points to {1}. Please \
            check the command syntax. If you need help, type .help to see how to use the \
            command.".format(points, userDisc), color=0xFF0000)
            await message.channel.send(embed=em)

    if message.content.startswith(".removepoints"):
        try:
            if message.author.permissions_in(message.channel).administrator:
                user = message.content[14:]
                userSplit = user.split('"')
                try:
                    userDisc = userSplit[1]
                except IndexError:
                    em = discord.Embed(title="Formatting error", description='Correct formatting: \n`.givepoints \
                    "username#descriminator" points`\ne.g. `.givepoints "alpha#1234" 100`\nYou can find a users\
                    username and discriminator by clicking on the users profile, it is positioned below the users \
                    server nickname.', color=0xFF0000)
                    await message.channel.send(embed=em)
                points = userSplit[2]
                if "#" not in userDisc or points is not points.isdigit():
                    print("Error: Use username and discriminator when using this function.")
                    em = discord.Embed(title="Formatting error", description='Correct formatting: \n`.removepoints \
                    "username#descriminator" points`\ne.g. `.removepoints "alpha#1234" 100`\nYou can find a users\
                     username and discriminator by clicking on the users profile, it is positioned below the users \
                     server nickname.', color=0xFF0000)
                    await message.channel.send(embed=em)
                else:
                    for x in client.get_all_members():
                        if (x.name + "#" + x.discriminator) == userDisc:
                            removePoints(x.id, points)
                            em= discord.Embed(title="Successfully removed points.", description="I have removed {0} \
                            points from {1}.".format(points, userDisc), color=0x008000)
                            await message.channel.send(embed=em)
        except:
            user = message.content[12:]
            userSplit = user.split(" ")
            userDisc = userSplit[0]
            points = userSplit[1]
            em = discord.Embed(title="Could not remove points.", description="Could not remove {0} points to \
            {1}. Please check the command syntax. If you need help, type .help to see how to use the \
            command.".format(points, userDisc), color=0xFF0000)
            await message.channel.send(embed=em)

    if message.content.startswith(".info"):
        user = message.content[6:]
        userSplit = user.split('"')
        try:
            userDisc = userSplit[1]
        except IndexError:
            em = discord.Embed(title="Formatting error", description='Correct formatting: \n`.info \
            "username#descriminator"`\ne.g. `.info "alpha#1234"`\nYou can find a users\
            username and discriminator by clicking on the users profile, it is positioned below the users \
            server nickname.', color=0xFF0000)
            await message.channel.send(embed=em)
        if "#" not in userDisc:
            print("Error: Use username and discriminator when using this function.")
            em = discord.Embed(title="Formatting error", description='Correct formatting: \n`.info \
            "username#descriminator"`\ne.g. `.info "alpha#1234"`\nYou can find a users\
            username and discriminator by clicking on the users profile, it is positioned below the users \
            server nickname.', color=0xFF0000)
            await message.channel.send(embed=em)
        else:
            for x in client.get_all_members():
                if (x.name + "#" + x.discriminator) == userDisc:
                    userUsername, userPoints, userJoinDate, userAvatarURL, userRoles = lookupUser(x.id)


client.run(secrets.TOKEN)

# embed help:
# https://cog-creators.github.io/discord-embed-sandbox/
