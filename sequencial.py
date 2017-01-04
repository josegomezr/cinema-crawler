# encoding=utf8
import crawlers
import json
import pickle
import threading
import time
import os
import shutil


result = {
  'chains': {},
  'theaters': {},
  'movies': {}
}

if __name__ == '__main__':

  try:
    shutil.rmtree('./tmp')
  except (FileNotFoundError, FileExistsError):
    pass

  try:
    os.mkdir('./tmp')
    os.mkdir('./tmp/responses')
    os.mkdir('./tmp/dumps')
    os.mkdir('./tmp/jsons')
  except (FileNotFoundError, FileExistsError):
    pass

  crawlers = [
    crawlers.CinepolisCrawler(),
    crawlers.CineramaCrawler(),
    crawlers.CinestarCrawler(),
    crawlers.CineplanetCrawler(),
    crawlers.MovieTimeCrawler(),
    crawlers.MultiCineJMCrawler(),
    crawlers.UVKMultiCineCrawler(),
    crawlers.CinemarkCrawler()
  ]

  threads = []
  for crawl in crawlers[0:1]:
    print ("[%s] Start" % crawl.name)
    crawl.getTheaters()
    crawl.getMovies()
    print ("[%s] Finish" % crawl.name)
    
    print ("[%s] Writing pickle dump" % crawl.name)
    with open('./tmp/dumps/%s.dump' % crawl.name, 'wb') as f:
      pickle.dump(crawl.model, f, protocol=3)
    
    print ("[%s] Writing json dump" % crawl.name)
    with open('./tmp/jsons/%s.json' % crawl.name, 'w') as f:
      json.dump(crawl.model.toJSON(), f)
    
    print ("[%s] Merging model with root" % crawl.name)

    chainHash = hex(hash(crawl.model))
    result['chains'][chainHash] = crawl.model.toJSON(False)
    
    for theater in crawl.model.theaters:
      theaterHash = hex(hash(theater))

      result['theaters'][theaterHash] = theater.toJSON(False)

      for movie in theater.movies:
        movieHash = hex(hash(movie))
        movieJSON = movie.toJSON()
        movieShowTimes = movieJSON['showtimes']
        if not result['movies'].get(movieHash):
          movieJSON['showtimes'] = {}
          result['movies'][movieHash] = movieJSON
        damovie = result['movies'][movieHash]
        damovie['showtimes'][theaterHash] = movieShowTimes

        if not chainHash in damovie['chains']:
          damovie['chains'].append(chainHash)

        if not theaterHash in damovie['theaters']:
          damovie['theaters'].append(theaterHash)

        result['movies'][movieHash] = damovie

  output = json.dumps(result)

  chainID = 1
  theaterID = 1
  movieID = 1

  for key, chain in result['chains'].items():
    output = output.replace(key, str(chainID))
    chainID = chainID + 1

  for key, theater in result['theaters'].items():
    output = output.replace(key, str(theaterID))
    theaterID = theaterID + 1

  for key, movie in result['movies'].items():
    output = output.replace(key, str(movieID))
    movieID = movieID + 1

  with open('tmp/result.json', 'w') as f:
    f.write(output)

  print("--- EXIT --- ")
