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
            movieHash = hex((hash(movie))

            if not result['movies'].get(movieHash):
              movieJSON = movie.toJSON()
              movieJSON['chains'] = [chainHash]
              movieJSON['theaters'] = [theaterHash]
              result['movies'][movieHash] = movieJSON
            
            if not chainHash in result['movies'][movieHash]['chains']:
              result['movies'][movieHash]['chains'].append(chainHash)

            if not theaterHash in result['movies'][movieHash]['theaters']:
              result['movies'][movieHash]['theaters'].append(theaterHash)

        Lock.release()
        BusyLock.release()
        print ("Exiting ", self.threadID)

if __name__ == '__main__':
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

  BusyLock.acquire()

  with open('tmp/result.json', 'w') as f:
    json.dump(result, f)

  BusyLock.release()