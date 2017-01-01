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

        result['chains'][hash(self.instance.model)] = self.instance.model.toJSON(False)
        
        for theater in self.instance.model.theaters:
          result['theaters'][hash(theater)] = theater.toJSON(False)

          for movie in theater.movies:
            result['movies'][hash(movie)] = movie.toJSON(False)

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
    th.join()

  with open('tmp/result.json', 'w') as f:
    json.dump(result, f)
