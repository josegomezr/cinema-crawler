import crawlers
import json

if __name__ == '__main__':
  crawler = crawlers.CineramaCrawler()
  crawler.getTheaters()
  crawler.getMovies()
  js = json.dump(crawler.model.toJSON(), open('cinerama.json', 'w'))


