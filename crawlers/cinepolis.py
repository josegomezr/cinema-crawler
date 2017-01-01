from . import base
from os import path
from .lib import schemas
from .lib import utils
import json

class CinepolisCrawler(base.BaseCrawler):
  def __init__(self):
    super(CinepolisCrawler, self).__init__('cinepolis')
    self.base_url = 'http://www.cinepolis.com.pe/'
    self.url = path.join(self.base_url, 'manejadores/CiudadesComplejos.ashx')
    self.model = schemas.Chain('cinepolis', self.url)

  def getTheaters(self):
    self.log('get-theaters')
    jsonCity = self.doRequest(self.url).json()
    # jsonCity = json.load(open('../test-files/cinepolis-json-1.json'))

    cinemas = []

    for obj in jsonCity:
      payload = {"claveCiudad": obj['Clave'], "esVIP": False}
      url = path.join(self.base_url, 'Cartelera.aspx/GetNowPlayingByCity')
      jsonCinemas = self.doRequest(url, method='post', json=payload).json()
      # jsonCinemas = json.load(open('../test-files/cinepolis-json-2.json'))
      cinemas.extend(jsonCinemas['d']['Cinemas'])
    
    for cinema in cinemas:
      self.model.addTheater( cinema['Name'], storage = cinema )
    
  def getMovies(self):
    for theater in self.model.theaters:
      self.log('get-movies-for-theater: %s' % theater.name)
      for dateDetail in theater.storage['Dates']:
        if utils.cinepolis_today() != dateDetail['ShowtimeDate']:
          continue
        for movieDetail in dateDetail['Movies']:
          showTimes = []
          meta = {}
          for movieFormatDetail in movieDetail['Formats']:
            meta['format'] = movieFormatDetail['Name']
            meta['language'] = movieFormatDetail['Language']
            for showTimeDetail in movieFormatDetail['Showtimes']:
              showTimes.append(showTimeDetail['Time'])
          meta['rating'] = movieDetail['Rating']
          meta['poster'] = movieDetail['Poster']
          title = movieDetail['Title']

          theater.addMovie(title, None, showTimes, meta)

