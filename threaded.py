# encoding=utf8
import crawlers
import threading

result = {
  'chains': {},
  'theaters': {},
  'movies': {}
}

Lock = threading.Lock()

if __name__ == '__main__':
  crawlers.lib.runner.prepare_fs()

  crawler_list = [crawl() for crawl in crawlers.__all__]

  threads = []
  for crawl in crawler_list:
    th = crawlers.lib.runner.Worker(crawl.name, crawl, Lock, result)
    threads.append (th)
    th.start()

  for thread in threads:
    thread.join()
    thread.instance.log('END')

  output = crawlers.lib.runner.replace_hashes_by_ids(result)
  with open('tmp/result.json', 'w') as f:
    f.write(output)

  print("--- EXIT --- ")