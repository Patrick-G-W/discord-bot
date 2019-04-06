from imdb import IMDb

ia = IMDb()

def search(message):
    movieSearch = message[6:]
    movie = ia.search_movie(movieSearch)
    movieID = movie[0].movieID
    getMovie = ia.get_movie(movieID)
    movieTitle = getMovie['title']
    movieURL = ia.get_imdbURL(movie[0])
    try:
        movieThumbURL = getMovie['cover url']
    except:
        movieThumbURL = "images.unknown.png"
        #movieThumbURL = "https://images.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
    moviePlot = str(getMovie['plot'][0])
    try:
        movieRelease = getMovie['year']
    except:
        movieRelease = "Unknown"
    try:
        movieScore = getMovie['rating']
    except:
        movieScore = "Unknown"
    try:
        movieGenre = ", ".join(getMovie['genres'])
    except:
        movieGenre = "Unknown"
    limitMoviePlot = moviePlot[:1000] + (moviePlot[1000:] and '...')
    return movieTitle, movieURL, movieThumbURL, limitMoviePlot, movieRelease, movieScore, movieGenre

