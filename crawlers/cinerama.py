from . import base
from os import path
from .lib import schemas

class CineramaCrawler(base.BaseCrawler):
  def __init__(self):
    super(CineramaCrawler, self).__init__('cinerama')
    self.base_url = 'http://www.cinerama.com.pe/'
    self.url = path.join(self.base_url, 'cines.php')
    self.model = schemas.Chain('cinerama', self.url)

  def getTheaters(self):
    soup = self.urlToBS4(self.url)
    self.log('get-theaters')
    for i in soup.select('p.titulo-tienda'):
      name = i.next.next.strip()
      href = path.join(self.base_url, i.next['href'])
      self.model.addTheater( name, href )

  def getMovies(self):
    self.log('get-movies')
    for theater in self.model.theaters:
      self.log('get-movies-for-theater: %s' % theater.name)
      soup = self.urlToBS4(theater.url)
      for movieDetail in soup.select('div.txt-cartelera'):
        title = movieDetail.select_one('div.titcarte').a.string
        description = movieDetail.select_one('p').string
        showtimes = movieDetail.select_one('div.horasprof').string
        showtimes = [i.strip() for i in showtimes.split('/')]
        theater.addMovie(title, description, showtimes)