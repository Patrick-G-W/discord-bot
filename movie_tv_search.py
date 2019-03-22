from imdb import IMDb
from dhooks import Webhook
import json

ia = IMDb()

def search(message):
    movieSearch = message[6:]
    movie = ia.search_movie(movieSearch)
    movieTitle = str(movie[0])
    movieID = movie[0].movieID
    movieURL = ia.get_imdbURL(movie[0])
    movieThumbURL = (ia.get_movie(movieID))['cover url']
    moviePlot = str((ia.get_movie(movieID))['plot'][0])
    movieRelease = ia.get_movie(movieID)['year']
    movieScore = ia.get_movie(movieID)['rating']
    #movieGenre = ia.get_movie(movieID)['genres'].join(",")
    movieGenre = ", ".join(ia.get_movie(movieID)['genres'])
    limitMoviePlot = moviePlot[:1000] + (moviePlot[1000:] and '...')
    return movieTitle, movieURL, movieThumbURL, limitMoviePlot, movieRelease, movieScore, movieGenre

