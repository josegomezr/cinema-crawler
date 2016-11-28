from . import base
from os import path
from .lib import schemas

class CinemarkCrawler(base.BaseCrawler):
  def __init__(self):
    super(CinemarkCrawler, self).__init__('cinemark')
    self.base_url = 'http://www.cinemark-peru.com/'
    self.url = path.join(self.base_url, 'cines')
    self.model = schemas.Chain('cinemark', self.url)

  def getTheaters(self):
    soup = self.urlToBS4(self.url)
    self.log('get-theaters')
    for itemSoup in soup.select('div.item-block'):
      name = itemSoup.select_one('h2').text.strip()
      href = itemSoup.select_one('a')['href']
      self.model.addTheater( name, href )

  def getMovies(self):
    self.log('get-movies')
    for theater in self.model.theaters:
      self.log('get-movies-for-theater: %s' % theater.name)
      url = self.base_url + theater.url
      soup = self.urlToBS4(url)
      for movieDetail in soup.select('div.item2'):
        title = movieDetail.select_one('h3').text.strip()
        
        showtimeSoup = movieDetail.select('div.tabbody div')
        showtimes = []
        for showtime in showtimeSoup:
          showtimes.extend( [time.strip() for time in showtime.select_one('li').text.split('|')] )

        theater.addMovie(title, None, showtimes)