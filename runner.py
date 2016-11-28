import crawlers
import json

if __name__ == '__main__':
  crawler = crawlers.CinemarkCrawler()
  crawler.getTheaters()
  crawler.getMovies()
  js = json.dump(crawler.model.toJSON(), open('tmp/%s.json' % crawler.name, 'w'))


