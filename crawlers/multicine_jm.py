# encoding=utf8

from . import base
from os import path
from .lib import schemas
from .lib import utils

class MultiCineJMCrawler(base.BaseCrawler):
  def __init__(self):
    super(MultiCineJMCrawler, self).__init__('multicine-jm')
    self.base_url = 'http://multicineplazajesusmaria.com/'
    self.url = path.join(self.base_url, 'cine-cartelera.php')
    self.model = schemas.Chain('multicines-jm', self.url)

  def getTheaters(self):
    self.model.addTheater( 'multicine-jm', self.url )

  def getMovies(self):
    self.log('get-movies')
    for theater in self.model.theaters:
      self.log('get-movies-for-theater: %s' % theater.name)
      soup = self.urlToBS4(theater.url)
      for movieSoup in soup.select('div.ProMin'):

        title = str(movieSoup.select('a')[1].text).strip()
        meta = utils.get_meta_from_title(title)
        title = utils.clean_tags_from_title(title)

        href = movieSoup.select('a')[1]['href']
        url = path.join(self.base_url, href)

        detailSoup = self.urlToBS4(url)
        
        row = detailSoup.select_one('table').select('tr')[1:]
        showtimes = []
        for room in row:
          cells = room.select('td')
          room_name = str(cells[0].text).strip()
          room_showtimes = cells[1].text

          times = [showtime.strip() for showtime in room_showtimes.split( chr(0xa0)*2 )]
          times.pop()
          showtimes.extend(times)

        theater.addMovie(title, None, showtimes, meta)
