import crawlers
import json
import pickle
import threading
import time

class CrawlerThread (threading.Thread):
    def __init__(self, threadID, instance):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.instance = instance
    def run(self):
        print ("Starting ", self.threadID)
        self.instance.getTheaters()
        self.instance.getMovies()
        
        with open('tmp/pickle-%s.dump' % self.threadID, 'wb') as f:
          pickle.dump(self.instance.model, f, protocol=4)
        
        with open('tmp/json-%s.json' % self.threadID, 'w') as f:
            json.dump(self.instance.model.toJSON(), f)

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
