import crawlers
import json
import pickle
import threading
import time

result = {
  'chains': {},
  'theaters': {},
  'movies': {}
}
Lock = threading.Lock()

BusyLock = threading.RLock() 

class CrawlerThread (threading.Thread):
    def __init__(self, threadID, instance):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.instance = instance
    def run(self):
        print ("Starting ", self.threadID)
        BusyLock.acquire()
        self.instance.getTheaters()
        self.instance.getMovies()

        with open('tmp/pickle-%s.dump' % self.threadID, 'wb') as f:
          pickle.dump(self.instance.model, f, protocol=4)
        
        with open('tmp/json-%s.json' % self.threadID, 'w') as f:
            json.dump(self.instance.model.toJSON(), f)
        
        Lock.acquire()

        chainHash = hex(hash(self.instance.model))

        result['chains'][chainHash] = self.instance.model.toJSON(False)
        
        for theater in self.instance.model.theaters:
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

        Lock.release()
        BusyLock.release()
        print ("Exiting ", self.threadID)

if __name__ == '__main__':
  crawlers = [
    crawlers.CinepolisCrawler(),
    # crawlers.CineramaCrawler(),
    crawlers.CinestarCrawler(),
    # crawlers.CineplanetCrawler(),
    # crawlers.MovieTimeCrawler(),
    # crawlers.MultiCineJMCrawler(),
    # crawlers.UVKMultiCineCrawler(),
    crawlers.CinemarkCrawler()
  ]

  threads = []
  for crawl in crawlers:
    th = CrawlerThread(str(crawl.name), crawl)
    threads.append (th)
    th.start()

  BusyLock.acquire()

  output = json.dumps(result)

  chainID = 1
  theaterID = 1
  movieID = 1

  for chain in result['chains'].values():
    output = output.replace(chain, chainID)
    chainID = chainID + 1

  for theater in result['theaters'].values():
    output = output.replace(theater, theaterID)
    theaterID = theaterID + 1

  for movie in result['movies'].values():
    output = output.replace(movie, movieID)
    movieID = movieID + 1

  with open('tmp/result.json', 'w') as f:
    f.write(output)

  BusyLock.release()