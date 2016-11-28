from . import base
from os import path
from .lib import schemas
from .lib import utils

class UVKMultiCineCrawler(base.BaseCrawler):
  def __init__(self):
    super(UVKMultiCineCrawler, self).__init__('uvk')
    self.base_url = 'http://www.uvkmulticines.com/'
    self.url = path.join(self.base_url, 'multicines/')
    self.model = schemas.Chain(self.name, self.url)

  def getTheaters(self):
    soup = self.urlToBS4(self.url)
    # soup = self.makeBS4(open('../test-files/uvk-cines.html'))

    for theaterSoup in soup.select("table table table table"):
      if not theaterSoup.select_one('h3'):
        continue

      title = str(theaterSoup.select_one('h3').text)
      url = theaterSoup.select('a')[1]['href']
      # url = path.join(self.base_url, url)
      
      # print (title, url)

      self.model.addTheater(title, url)

  def getMovies(self):
    url = path.join(self.base_url, 'cartelera/')
    # soup = self.makeBS4(open('../test-files/uvk-movies.html'))
    soup = self.urlToBS4(url)

    movies = {}
    for movieSoup in soup.select("table table table"):
      if not movieSoup.select('.bg_titulista_negro'):
        continue
      
      key = movieSoup.select_one('a')['href']
      name = movieSoup.select_one('.bg_titulista_negro h3').text.strip()
      
      description = movieSoup.select_one('p').next.next.next.next.next.strip()

      metas = {}
      for metaSoup in movieSoup.select('div.version'):
        meta = metaSoup.next 
        meta = ' '.join(meta.strip().split(' ')[1:-1])
        for submeta in meta.split(' - '):
          metas[submeta.strip()] = True

      movies[key] = {
        'titulo': name,
        'href': key,
        'description': description,
        'meta' : metas
      }

    for href, movieDict in movies.items():
      url = path.join(self.base_url, href)
      movieSoup = self.urlToBS4(url)
      # movieSoup = self.makeBS4(open('../test-files/uvk-detail-movie.html'))
      cinemas = movieSoup.select("table table table table table")[1].select('a')

      for theater in self.model.theaters:
        for cinema in cinemas:
          if cinema['href'] == theater.url:
            theater.addMovie(
              movieDict['titulo'], 
              movieDict['description'], 
              [], 
              movieDict['meta']
            )
