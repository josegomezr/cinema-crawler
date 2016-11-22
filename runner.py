import crawlers
import json

if __name__ == '__main__':
  crawler = crawlers.CineplanetCrawler()
  crawler.getTheaters()
  crawler.getMovies()
  js = json.dump(crawler.model.toJSON(), open('cineplanet.json', 'w'))


