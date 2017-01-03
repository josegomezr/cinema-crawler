# encoding=utf8

from . import base
from os import path
from .lib import schemas
from bs4 import BeautifulSoup
from .lib import utils

class MovieTimeCrawler(base.BaseCrawler):
  def __init__(self):
    super(MovieTimeCrawler, self).__init__('movietime')
    self.base_url = 'http://www.movietime.com.pe//'
    self.url = path.join(self.base_url, 'multicines')
    self.model = schemas.Chain('movietime', self.url)

  def getTheaters(self):
    soup = self.urlToBS4(self.url)
    # soup = BeautifulSoup(open('../test-files/cinestar-multicines.html', 'r').read(), 'html.parser')
    self.log('get-theaters')

    for i in soup.select('div.caja_pelicula'):
      name = i.select_one('h4').text
      href = i.select_one('div.iconos_link').select_one('a')['href']
      self.model.addTheater( name, href )

  def getMovies(self):
    self.log('get-movies')
    for theater in self.model.theaters:
      self.log('get-movies-for-theater: %s' % theater.name)
      soup = self.urlToBS4(theater.url)
      # soup = BeautifulSoup(open('../test-files/cinestar-cine-detalle.html', 'r').read(), 'html.parser')
      
      for row in soup.select_one('#programacionneo').select('tr'):
        if row.th:
          continue
        
        title = utils.clean_tags_from_title(row.td.text)
        meta = utils.get_meta_from_title(title)
        showtimes = [time.strip() for time in row.td.nextSibling.text.split('/')]
        theater.addMovie(title, None, showtimes, meta)

