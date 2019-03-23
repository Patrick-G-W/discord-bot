from imdb import IMDb

ia = IMDb()

def search(message):
    movieSearch = message[6:]
    movie = ia.search_movie(movieSearch)
    movieID = movie[0].movieID
    getMovie = ia.get_movie(movieID)
    movieTitle = getMovie['title']
    movieURL = ia.get_imdbURL(movie[0])
    movieThumbURL = getMovie['cover url']
    moviePlot = str(getMovie['plot'][0])
    movieRelease = getMovie['year']
    movieScore = getMovie['rating']
    movieGenre = ", ".join(getMovie['genres'])
    limitMoviePlot = moviePlot[:1000] + (moviePlot[1000:] and '...')
    return movieTitle, movieURL, movieThumbURL, limitMoviePlot, movieRelease, movieScore, movieGenre

