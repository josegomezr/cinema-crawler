import crawlers
import json

if __name__ == '__main__':
  crawler = crawlers.MultiCineJMCrawler()
  crawler.getTheaters()
  crawler.getMovies()
  js = json.dump(crawler.model.toJSON(), open('%s.json' % crawler.name, 'w'))


