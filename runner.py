import crawlers
import json

if __name__ == '__main__':
  crawler = crawlers.CinestarCrawler()
  crawler.getTheaters()
  crawler.getMovies()
  js = json.dump(crawler.model.toJSON(), open('cinestar.json', 'w'))


