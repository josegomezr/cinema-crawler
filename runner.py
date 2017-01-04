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
Lock = threading.Lock()

class CrawlerThread (threading.Thread):
    def __init__(self, threadID, instance):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.instance = instance
        
    def run(self):
        print ("[%s] Start" % self.threadID)
        self.instance.getTheaters()
        self.instance.getMovies()
        print ("[%s] Finish" % self.threadID)
        

        print ("[%s] Writing pickle dump" % self.threadID)
        with open('tmp/dumps/%s.dump' % self.threadID, 'wb') as f:
          pickle.dump(self.instance.model, f, protocol=4)
        
        print ("[%s] Writing json dump" % self.threadID)
        with open('tmp/jsons/%s.json' % self.threadID, 'w') as f:
          json.dump(self.instance.model.toJSON(), f)
        
        print ("[%s] Merging model with root" % self.threadID)
        Lock.acquire()

        chainHash = hex(hash(self.instance.model))
        result['chains'][chainHash] = self.instance.model.toJSON(False)
        
        for theater in self.instance.model.theaters:
          theaterHash = hex(hash(theater))

          # print(theaterHash, theater.name)

          result['theaters'][theaterHash] = theater.toJSON(False)

          for movie in theater.movies:
            movieHash = hex(hash(movie))
            # print("--", movieHash, movie.name)
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

        Lock.release()
        print ("[%s] End" % self.threadID)

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
  for crawl in crawlers:
    th = CrawlerThread(str(crawl.name), crawl)
    threads.append (th)
    th.start()

  for thread in threads:
    thread.join()
    thread.instance.log('END')

  output = json.dumps(result)

  chainID = 1
  theaterID = 1
  movieID = 1

  for key, chain in result['chains'].items():
    # print(key, chain)
    output = output.replace(key, str(chainID))
    chainID = chainID + 1

  for key, theater in result['theaters'].items():
    # print(key, theater)
    output = output.replace(key, str(theaterID))
    theaterID = theaterID + 1

  for key, movie in result['movies'].items():
    # print(key, movie)
    output = output.replace(key, str(movieID))
    movieID = movieID + 1

  with open('tmp/result.json', 'w') as f:
    f.write(output)
