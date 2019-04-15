import sqlite3
import os
import time

database_path = './database'
filename = 'userDatabase'

os.makedirs(database_path, exist_ok=True)

db = sqlite3.connect('./database/userDatabase.sqlite3')

def createDatabase(idList):
    print("Creating database if not already there...")
    db.execute('CREATE TABLE IF NOT EXISTS users (db_id INTEGER PRIMARY KEY, user_id INTEGER UNIQUE, userName TEXT, points INTEGER DEFAULT 0, joinDate TEXT, avatarURL TEXT, roles TEXT)')
    print("Database found/created.")
    time.sleep(1)
    print("Inserting new users into database...")
    for x in idList:
        roles = ', '.join(str(e) for e in x.roles)
        db.execute('INSERT OR IGNORE INTO users (user_id, userName, joinDate, avatarURL, roles) VALUES ({0},"{1}","{2}","{3}","{4}")'.format(x.id, x.name, str(x.joined_at)[:23], x.avatar_url, roles))
    db.commit()


def insertNewUserIntoDatabase(userID, joinedAt, avatar_url, roles, name):
    print("Connected to database.")
    db.execute('INSERT OR IGNORE INTO users (user_id, userName, joinDate, avatarURL, roles) VALUES ({0},"{1}","{2}","{3}","{4}")'.format(userID, name, joinedAt, avatar_url, roles))
    db.commit()
    print("Added new user to database.")


def removeRedundantUsers(idList, userName):
    print("Attempting to remove {0} from the database...".format(userName))
    print("Using ID {0} to remove user.".format(idList))
    db.execute('DELETE FROM users WHERE user_id = {0}'.format(idList))
    db.commit()
    print("User {0} has been removed from the database.".format(userName))


def updateDatabase(idList):
    print("Updating table with new data...")
    print("Adding new users if there are any...")
    for x in idList:
        roles = ', '.join(str(e) for e in x.roles)
        db.execute('UPDATE users SET userName = "{0}", avatarURL = "{1}", roles = "{2}" WHERE user_id = {3}'.format(x.name, x.avatar_url, roles, x.id))
        db.execute('INSERT OR IGNORE INTO users (user_id, userName, joinDate, avatarURL, roles) VALUES ({0},"{1}","{2}","{3}","{4}")'.format(x.id, x.name, str(x.joined_at)[:23], x.avatar_url, roles))
        db.commit()
    print("Done adding new users.")
    print("Finished updating table.")


def givePoints(userID, points):
    db.execute('UPDATE users SET points = points + {0} WHERE user_id = "{1}"'.format(points, userID))
    print("Gave {0} points to {1}.".format(points, userID))
    db.commit()


def removePoints(userID, points):
    db.execute('UPDATE users SET points = points - {0} WHERE user_id = "{1}"'.format(points, userID))
    print("Removed {0} points from {1}.".format(points, userID))
    db.commit()
