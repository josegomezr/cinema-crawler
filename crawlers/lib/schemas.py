from . import utils
class Chain:
  def __init__(self, name, url):
    self.name = name
    self.url = url
    self.theaters = []

  def addTheater(self, name, url= None, storage=None):
    obj = Theater(name, url, storage)
    obj.chain = hex(hash(self))
    self.theaters.append(obj)

  def __hash__(self):
    return hash(self.name.lower())

  def toJSON(self, deep = True):
    obj = {
      'id' : hex(hash(self)),
      'name': self.name
    }
    if deep:
      theaters = [ theater.toJSON() for theater in self.theaters ]
      obj['theaters'] = theaters

    return obj

class Theater:
  def __init__(self, name, url = None, storage=None):
    self.name = name
    self.url = url
    self.movies = []
    self.storage = storage

  def addMovie(self, name, description, showtimes, meta={}):
    obj = Movie(name, description, showtimes, **meta)
    obj.theater = hex(hash(self))
    obj.chain = self.chain
    self.movies.append(obj)

  def __hash__(self):
    return hash((self.chain, self.name.lower()))

  def toJSON(self, deep = True):
    obj = {
      'id' : hex(hash(self)),
      'name': self.name,
      'url': self.url,
      'chain': self.chain
    }

    if deep:
      obj['movies'] = [movie.toJSON() for movie in self.movies]

    return obj

class Movie:
  def __init__(self, name, description, showtimes, **kwargs):
    self.name = name
    self.showtimes = [ShowTime(i) for i in showtimes]
    self.meta = kwargs

  def toJSON(self):
    return {
      'id' : hex(hash(self)),
      'name': utils.clean_tags_from_title(self.name),
      'showtimes': [showtime.toJSON() for showtime in self.showtimes],
      'theaters': [],
      'chains': [],
      'meta': self.meta
    }

  def __eq__(self, rhs):
    return utils.clean_tags_from_title(self.name) == utils.clean_tags_from_title(rhs.name)
  
  def __hash__(self):
    return hash(utils.clean_tags_from_title(self.name).lower())

class ShowTime:
  def __init__(self, showtime):
    self.showtime = showtime

  def toJSON(self):
    return self.showtime
