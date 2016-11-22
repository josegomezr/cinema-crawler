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

  def getTheaters(self):
    self.log('get-theaters')
    # jsonCity = self.doRequest(self.url).json()
    soup = self.makeBS4(open('../test-files/cineplanet-main.html').read())

    chain = []

    for item in soup.select_one('.WEB_CONTE_menu').select('li')[4].select('li'):
      chain.append( [item.a.text, item.a['href']] )
      break
    
    for city in chain:

      soup = self.makeBS4(open('../test-files/cineplanet-ciudad.html').read())
      for item in soup.select('.WEB_cineListadoItem'):
        name = item.select_one('.WEB_cineListadoNombre').a.text
        href = item.select_one('.WEB_cineListadoNombre').a['href']
        href = path.join(self.url, href)
        self.model.addTheater( name, href )

    
  def getMovies(self):
    for theater in self.model.theaters:
      theater.url 
      # self.log('get-movies-for-theater: %s' % theater.name)
      # for dateDetail in theater.storage['Dates']:
      #   if utils.cinepolis_today() != dateDetail['ShowtimeDate']:
      #     continue
      #   for movieDetail in dateDetail['Movies']:
      #     showTimes = []
      #     meta = {}
      #     for movieFormatDetail in movieDetail['Formats']:
      #       meta['format'] = movieFormatDetail['Name']
      #       meta['language'] = movieFormatDetail['Language']
      #       for showTimeDetail in movieFormatDetail['Showtimes']:
      #         showTimes.append(showTimeDetail['Time'])
      #     meta['rating'] = movieDetail['Rating']
      #     meta['poster'] = movieDetail['Poster']
      #     title = movieDetail['Title']

      #     theater.addMovie(title, None, showTimes, meta)

