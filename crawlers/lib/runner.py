import pickle
import json
import os
import shutil
import threading

def run_crawler(crawler):
  print ("[%s] Start" % crawler.name)
  crawler.getTheaters()
  crawler.getMovies()
  print ("[%s] Finish" % crawler.name)
  
  print ("[%s] Writing pickle dump" % crawler.name)
  with open('./tmp/dumps/%s.dump' % crawler.name, 'wb') as f:
    pickle.dump(crawler.model, f, protocol=3)
  
  print ("[%s] Writing json dump" % crawler.name)
  with open('./tmp/jsons/%s.json' % crawler.name, 'w') as f:
    json.dump(crawler.model.toJSON(), f)

  return crawler.model

def merge_crawler_result(result, crawler):
  print ("[%s] Merging model with root" % crawler.name)

  chainHash = hex(hash(crawler.model))
  result['chains'][chainHash] = crawler.model.toJSON(False)
  
  for theater in crawler.model.theaters:
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
      
      mergedShowtime = damovie['showtimes'].get(theaterHash, {})

      mergedShowtime.update({
        'theater': theaterHash,
        'showtime': movieShowTimes,
        'movie' : damovie['id']
      })

      damovie['showtimes'][theaterHash] = mergedShowtime

      if not chainHash in damovie['chains']:
        damovie['chains'].append(chainHash)

      if not theaterHash in damovie['theaters']:
        damovie['theaters'].append(theaterHash)

      result['movies'][movieHash] = damovie

def replace_hashes_by_ids(result):
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

  return output

def prepare_fs():
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


class Worker (threading.Thread):
  def __init__(self, threadID, instance, mergeLock, result):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.instance = instance
    self.mergeLock = mergeLock
    self.result = result
      
  def run(self):
    run_crawler(self.instance)

    self.mergeLock.acquire()
    merge_crawler_result(self.result, self.instance)
    self.mergeLock.release()
    print ("[%s] End" % self.threadID)