from . import base
from os import path
from .lib import schemas
from .lib import utils
import json

class CineplanetCrawler(base.BaseCrawler):
  def __init__(self):
    super(CineplanetCrawler, self).__init__('cineplanet')
    self.base_url = 'https://cineplanet.com.pe/'
    self.url = path.join(self.base_url, '')
    self.model = schemas.Chain('cineplanet', self.url)
    self.headers = {
      'user-agent':  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " + \
                     "(KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36"
      }

  def getTheaters(self):
    self.log('get-theaters')
    # soup = self.makeBS4(open('../test-files/cineplanet-main.html').read())
    
    soup = self.urlToBS4(self.url, headers = self.headers)

    chain = []

    # all cities
    for item in soup.select_one('.WEB_CONTE_menu').select('li')[4].select('li'):
      chain.append( item.a['href'] )
    
    # from each city
    for city in chain:
      # soup = self.makeBS4(open('../test-files/cineplanet-ciudad.html').read())

      soup = self.urlToBS4("%s%s" % (self.base_url, city), headers = self.headers)
      # get all theater
      for item in soup.select('.WEB_cineListadoItem'):
        name = item.select_one('.WEB_cineListadoNombre').a.text
        href = item.select_one('.WEB_cineListadoNombre').a['href']
        href = self.url+href
        self.model.addTheater( name, href )
    
  def getMovies(self):
    # from each theater
    for theater in self.model.theaters:
      # get all movies
      self.log('get-movies-for-theater: %s' % theater.name)
      soup = self.urlToBS4(theater.url, headers = self.headers)
      # soup = self.makeBS4(open('../test-files/cineplanet-cine.html').read())
      for movieSoup in soup.select(".WEB_cineCarteleraDetalle"):
        title = str(movieSoup.select_one('.WEB_cinePeliculaNombre').next).strip()
        showtimes = [ i.text for i in movieSoup.select('.horarioDisponible') ]
        print (showtimes)

        theater.addMovie(title, None, showtimes )
