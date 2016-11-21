class Chain:
  def __init__(self, name, url):
    self.name = name
    self.url = url
    self.theaters = []

  def addTheater(self, name, url= None, storage=None):
    self.theaters.append(Theater(name, url, storage))

  def toJSON(self):
    return {
      'name': self.name,
      'theaters': [ theater.toJSON() for theater in self.theaters ]
    }

class Theater:
  def __init__(self, name, url = None, storage=None):
    self.name = name
    self.url = url
    self.movies = []
    self.storage = storage
  def addMovie(self, name, description, showtimes, meta={}):
    self.movies.append(Movie(name, description, showtimes, **meta))
  def toJSON(self):
    return {
      'name': self.name,
      'movies': [movie.toJSON() for movie in self.movies]
    }

class Movie:
  def __init__(self, name, description, showtimes, **kwargs):
    self.name = name
    self.showtimes = [ShowTime(i) for i in showtimes]
    self.meta = kwargs
  def toJSON(self):
    return {
      'name': self.name,
      'showtimes': [showtime.toJSON() for showtime in self.showtimes],
      'meta': self.meta
    }

class ShowTime:
  def __init__(self, showtime):
    self.showtime = showtime
  def toJSON(self):
    return self.showtime
