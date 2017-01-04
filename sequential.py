# encoding=utf8
import crawlers

result = {
  'chains': {},
  'theaters': {},
  'movies': {}
}

if __name__ == '__main__':
  crawlers.lib.runner.prepare_fs()
  crawler_list = [crawl() for crawl in crawlers.__all__]

  for crawl in crawler_list:
    crawlers.lib.runner.run_crawler(crawl)
    crawlers.lib.runner.merge_crawler_result(result, crawl)

  output = crawlers.lib.runner.replace_hashes_by_ids(result)
  with open('tmp/result.json', 'w') as f:
    f.write(output)

  print("--- EXIT --- ")
